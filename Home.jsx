/**
 * @file Home page component for the Math Grid Puzzle Game
 * @description Enhanced game with timed and guesses modes, centered target, and immediate feedback
 */

import React, { useState, useEffect, useCallback } from 'react';
import { Play, RotateCcw, Clock, Target, Timer, Hash } from 'lucide-react';

/**
 * Main game component with centered target and two game modes
 */
export default function Home() {
  const [gameState, setGameState] = useState({
    grid: [],
    target: 0,
    selectedCells: [],
    timeLeft: 300,
    isPlaying: false,
    score: 0,
    message: 'Select game mode and click Play!',
    gameMode: 'timed',
    guessesLeft: 20,
    correctGuesses: 0,
    startTime: null
  });

  /**
   * Generate a 10x10 grid with random numbers 0-9
   */
  const generateGrid = useCallback(() => {
    const grid = [];
    for (let i = 0; i < 10; i++) {
      const row = [];
      for (let j = 0; j < 10; j++) {
        row.push({
          value: Math.floor(Math.random() * 10),
          isSelected: false,
          row: i,
          col: j
        });
      }
      grid.push(row);
    }
    return grid;
  }, []);

  /**
   * Generate target number from the grid using game rules
   */
  const generateTarget = useCallback((grid) => {
    const lines = [];

    // Horizontal lines
    for (let i = 0; i < 10; i++) {
      for (let j = 0; j < 8; j++) {
        lines.push([grid[i][j], grid[i][j + 1], grid[i][j + 2]]);
      }
    }

    // Vertical lines
    for (let i = 0; i < 8; i++) {
      for (let j = 0; j < 10; j++) {
        lines.push([grid[i][j], grid[i + 1][j], grid[i + 2][j]]);
      }
    }

    // Diagonal lines (top-left to bottom-right)
    for (let i = 0; i < 8; i++) {
      for (let j = 0; j < 8; j++) {
        lines.push([grid[i][j], grid[i + 1][j + 1], grid[i + 2][j + 2]]);
      }
    }

    // Diagonal lines (top-right to bottom-left)
    for (let i = 0; i < 8; i++) {
      for (let j = 2; j < 10; j++) {
        lines.push([grid[i][j], grid[i + 1][j - 1], grid[i + 2][j - 2]]);
      }
    }

    const randomLine = lines[Math.floor(Math.random() * lines.length)];
    const [first, second, third] = randomLine;
    const operation = Math.random() > 0.5 ? 'add' : 'subtract';
    
    return operation === 'add' 
      ? first.value * second.value + third.value
      : first.value * second.value - third.value;
  }, []);

  /**
   * Initialize new game state
   */
  const startGame = useCallback(() => {
    const grid = generateGrid();
    const target = generateTarget(grid);
    const initialTime = gameState.gameMode === 'timed' ? 300 : 0;
    const initialGuesses = gameState.gameMode === 'guesses' ? 20 : 0;
    
    setGameState(prev => ({
      ...prev,
      grid,
      target,
      selectedCells: [],
      timeLeft: initialTime,
      guessesLeft: initialGuesses,
      isPlaying: true,
      score: 0,
      correctGuesses: 0,
      startTime: Date.now(),
      message: `Find 3 numbers in a straight line! Mode: ${prev.gameMode}`
    }));
  }, [generateGrid, generateTarget, gameState.gameMode]);

  /**
   * Handle cell selection
   */
  const handleCellClick = (cell) => {
    if (!gameState.isPlaying) return;

    const { selectedCells, grid } = gameState;
    
    const newGrid = grid.map(row => 
      row.map(c => 
        c.row === cell.row && c.col === cell.col 
          ? { ...c, isSelected: !c.isSelected }
          : c
      )
    );

    let newSelectedCells;
    if (cell.isSelected) {
      newSelectedCells = selectedCells.filter(
        selected => !(selected.row === cell.row && selected.col === cell.col)
      );
    } else if (selectedCells.length < 3) {
      newSelectedCells = [...selectedCells, { ...cell, isSelected: true }];
    } else {
      newSelectedCells = [...selectedCells.slice(1), { ...cell, isSelected: true }];
    }

    setGameState(prev => ({
      ...prev,
      grid: newGrid,
      selectedCells: newSelectedCells
    }));

    if (newSelectedCells.length === 3) {
      checkSelection(newSelectedCells);
    }
  };

  /**
   * Check selected cells
   */
  const checkSelection = (selectedCells) => {
    const [first, second, third] = selectedCells;
    
    const isHorizontal = first.row === second.row && second.row === third.row &&
                        Math.abs(first.col - second.col) === 1 && 
                        Math.abs(second.col - third.col) === 1;
    
    const isVertical = first.col === second.col && second.col === third.col &&
                      Math.abs(first.row - second.row) === 1 && 
                      Math.abs(second.row - third.row) === 1;
    
    const isDiagonal1 = (first.row + 2 === third.row && first.col + 2 === third.col) ||
                       (first.row + 2 === third.row && first.col - 2 === third.col);
    
    const isDiagonal2 = (first.row - 2 === third.row && first.col + 2 === third.col) ||
                       (first.row - 2 === third.row && first.col - 2 === third.col);

    if (!isHorizontal && !isVertical && !isDiagonal1 && !isDiagonal2) {
      setGameState(prev => ({
        ...prev,
        message: 'Cells must be in a straight line (horizontal, vertical, or diagonal)!',
        selectedCells: [],
        grid: prev.grid.map(row => 
          row.map(cell => ({ ...cell, isSelected: false }))
        )
      }));
      return;
    }

    const addResult = first.value * second.value + third.value;
    const subtractResult = first.value * second.value - third.value;

    if (addResult === gameState.target || subtractResult === gameState.target) {
      const newGrid = generateGrid();
      const newTarget = generateTarget(newGrid);
      
      if (gameState.gameMode === 'timed') {
        setGameState(prev => ({
          ...prev,
          grid: newGrid,
          target: newTarget,
          selectedCells: [],
          correctGuesses: prev.correctGuesses + 1,
          score: prev.correctGuesses + 1,
          message: `Correct! Total correct: ${prev.correctGuesses + 1}`
        }));
      } else {
        setGameState(prev => {
          const newGuessesLeft = prev.guessesLeft - 1;
          const newCorrectGuesses = prev.correctGuesses + 1;
          
          if (newCorrectGuesses === 20) {
            const endTime = Date.now();
            const totalTime = (endTime - (prev.startTime || endTime)) / 1000;
            return {
              ...prev,
              isPlaying: false,
              score: totalTime,
              message: `Game Complete! Time: ${totalTime}`
            };
          }
          
          return {
            ...prev,
            grid: newGrid,
            target: newTarget,
            selectedCells: [],
            guessesLeft: newGuessesLeft,
            correctGuesses: newCorrectGuesses,
            message: `Correct! ${newGuessesLeft} guesses left`
          };
        });
      }
    } else {
      setGameState(prev => {
        const newGuessesLeft = prev.guessesLeft - 1;
        const endGame = prev.gameMode === 'guesses' && newGuessesLeft <= 0;
        const endTime = Date.now();
        const totalTime = (endTime - (prev.startTime || endTime)) / 1000;

        return {
          ...prev,
          selectedCells: [],
          grid: prev.grid.map(row => row.map(cell => ({ ...cell, isSelected: false }))),
          message: endGame
            ? `Game Over! Final time: ${totalTime}`
            : 'Wrong combination! Try again.',
          guessesLeft: prev.gameMode === 'guesses' ? newGuessesLeft : prev.guessesLeft,
          isPlaying: endGame ? false : prev.isPlaying,
          score: endGame ? totalTime : prev.score
        };
      });
    }
  };

  /**
   * Timer countdown effect
   */
  useEffect(() => {
    if (!gameState.isPlaying || gameState.gameMode !== 'timed' || gameState.timeLeft <= 0) return;

    const timer = setInterval(() => {
      setGameState(prev => {
        if (prev.timeLeft <= 1) {
          return {
            ...prev,
            timeLeft: 0,
            isPlaying: false,
            message: `Time's up! Final Score: ${prev.correctGuesses}`
          };
        }
        return { ...prev, timeLeft: prev.timeLeft - 1 };
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [gameState.isPlaying, gameState.timeLeft, gameState.gameMode]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Math Grid Puzzle</h1>
          <p className="text-gray-600">
            Find 3 numbers in a straight line where (1st × 2nd) ± 3rd = Target
          </p>
        </div>

        {/* Game Controls & Info Panel */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          {/* Game Mode Selection */}
          <div className="flex justify-center gap-4 mb-4">
            <button
              onClick={() => setGameState(prev => ({ ...prev, gameMode: 'timed' }))}
              className={`px-4 py-2 rounded-lg font-semibold transition-colors flex items-center gap-2 ${
                gameState.gameMode === 'timed'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
              disabled={gameState.isPlaying}
            >
              <Timer className="w-4 h-4" />
              Timed Mode
            </button>
            
            <button
              onClick={() => setGameState(prev => ({ ...prev, gameMode: 'guesses' }))}
              className={`px-4 py-2 rounded-lg font-semibold transition-colors flex items-center gap-2 ${
                gameState.gameMode === 'guesses'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
              disabled={gameState.isPlaying}
            >
              <Hash className="w-4 h-4" />
              Guesses Mode
            </button>
          </div>

          {/* Info and Grid */}
          {/* (Rest of the JSX stays identical to your TSX version) */}
        </div>
      </div>
    </div>
  );
}
