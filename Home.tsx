/**
 * @file Home page component for the Math Grid Puzzle Game
 * @description Enhanced game with timed and guesses modes, centered target, and immediate feedback
 */

import React, { useState, useEffect, useCallback } from 'react';
import { Play, RotateCcw, Clock, Target, Timer, Hash } from 'lucide-react';

/**
 * Type definitions for game state and grid structure
 */
interface GridCell {
  value: number;
  isSelected: boolean;
  row: number;
  col: number;
}

interface GameState {
  grid: GridCell[][];
  target: number;
  selectedCells: GridCell[];
  timeLeft: float;
  isPlaying: boolean;
  score: float;
  message: string;
  gameMode: 'timed' | 'guesses';
  guessesLeft: number;
  correctGuesses: number;
  startTime: float | null;
}

/**
 * Main game component with centered target and two game modes
 */
export default function Home() {
  const [gameState, setGameState] = useState<GameState>({
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
  const generateGrid = useCallback((): GridCell[][] => {
    const grid: GridCell[][] = [];
    for (let i = 0; i < 10; i++) {
      const row: GridCell[] = [];
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
  const generateTarget = useCallback((grid: GridCell[][]): number => {
    const lines: GridCell[][] = [];

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

    // Pick a random line and generate target
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
   * Handle cell selection in the grid
   */
  const handleCellClick = (cell: GridCell) => {
    if (!gameState.isPlaying) return;

    const { selectedCells, grid } = gameState;
    
    // Toggle selection
    const newGrid = grid.map(row => 
      row.map(c => 
        c.row === cell.row && c.col === cell.col 
          ? { ...c, isSelected: !c.isSelected }
          : c
      )
    );

    let newSelectedCells: GridCell[];
    if (cell.isSelected) {
      newSelectedCells = selectedCells.filter(
        selected => !(selected.row === cell.row && selected.col === cell.col)
      );
    } else if (selectedCells.length < 3) {
      newSelectedCells = [...selectedCells, { ...cell, isSelected: true }];
    } else {
      // Replace the oldest selection
      newSelectedCells = [...selectedCells.slice(1), { ...cell, isSelected: true }];
    }

    setGameState(prev => ({
      ...prev,
      grid: newGrid,
      selectedCells: newSelectedCells
    }));

    // Check if we have 3 selected cells
    if (newSelectedCells.length === 3) {
      checkSelection(newSelectedCells);
    }
  };

  /**
   * Check if selected cells form a valid combination
   */
  const checkSelection = (selectedCells: GridCell[]) => {
    const [first, second, third] = selectedCells;
    
    // Check if cells are in straight line
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

    // Check if combination matches target
    const addResult = first.value * second.value + third.value;
    const subtractResult = first.value * second.value - third.value;

    if (addResult === gameState.target || subtractResult === gameState.target) {
      // Correct guess - generate new grid and target
      const newGrid = generateGrid();
      const newTarget = generateTarget(newGrid);
      
      if (gameState.gameMode === 'timed') {
        // Timed mode: score is number of correct guesses
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
        // Guesses mode: score is time taken for 20 correct guesses
        const newGuessesLeft = prev => prev.guessesLeft - 1;
        const newCorrectGuesses = prev => prev.correctGuesses + 1;
        
        setGameState(prev => ({
          ...prev,
          grid: newGrid,
          target: newTarget,
          selectedCells: [],
          guessesLeft: newGuessesLeft(prev),
          correctGuesses: newCorrectGuesses(prev),
          message: `Correct! ${newGuessesLeft(prev)} guesses left`
        }));

        // Check if game is complete (20 correct guesses)
        if (newCorrectGuesses(gameState) === 20) {
          const endTime = Date.now();
          const totalTime = (endTime - (gameState.startTime || endTime)) / 1000;
          setGameState(prev => ({
            ...prev,
            isPlaying: false,
            score: totalTime,
            message: `Game Complete! Time: ${totalTime}`
          }));
        }
      }
    } else {
      // Wrong guess - immediately clear selection
      setGameState(prev => ({
        ...prev,
        selectedCells: [],
        grid: prev.grid.map(row => 
          row.map(cell => ({ ...cell, isSelected: false }))
        ),
        message: 'Wrong combination! Try again.',
        ...(prev.gameMode === 'guesses' && {
          guessesLeft: prev.guessesLeft - 1
        })
      }));

      // Check if guesses are exhausted in guesses mode
      if (gameState.gameMode === 'guesses' && gameState.guessesLeft - 1 <= 0) {
        const endTime = Date.now();
        const totalTime = (endTime - (gameState.startTime || endTime)) / 1000;
        setGameState(prev => ({
          ...prev,
          isPlaying: false,
          score: totalTime,
          message: `Game Over! Final time: ${totalTime}`
        }));
      }
    }
  };

  /**
   * Timer countdown effect for timed mode
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
        return {
          ...prev,
          timeLeft: prev.timeLeft - 1
        };
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [gameState.isPlaying, gameState.timeLeft, gameState.gameMode]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Math Grid Puzzle
          </h1>
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

          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
            {/* Game Mode Specific Info */}
            {gameState.gameMode === 'timed' ? (
              <>
                <div className="text-center">
                  <Clock className="w-8 h-8 text-red-500 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-gray-800">{gameState.timeLeft}</div>
                  <div className="text-sm text-gray-600">Time Left</div>
                </div>
                
                <div className="text-center">
                  <Hash className="w-8 h-8 text-green-500 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-green-600">{gameState.correctGuesses}</div>
                  <div className="text-sm text-gray-600">Correct</div>
                </div>
              </>
            ) : (
              <>
                <div className="text-center">
                  <Hash className="w-8 h-8 text-purple-500 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-purple-600">{gameState.guessesLeft}</div>
                  <div className="text-sm text-gray-600">Guesses Left</div>
                </div>
                
                <div className="text-center">
                  <Clock className="w-8 h-8 text-green-500 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-green-600">
                    {gameState.isPlaying && gameState.startTime 
                      ? (Date.now() - gameState.startTime) / 1000
                      : 0}
                  </div>
                  <div className="text-sm text-gray-600">Time</div>
                </div>
              </>
            )}
            
            {/* Score Display */}
            <div className="text-center">
              <Target className="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-blue-600">{gameState.score}</div>
              <div className="text-sm text-gray-600">
                {gameState.gameMode === 'timed' ? 'Score' : 'Time'}
              </div>
            </div>
          </div>

          {/* Control Buttons */}
          <div className="flex justify-center gap-4">
            <button
              onClick={startGame}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2"
            >
              {gameState.isPlaying ? <RotateCcw className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              {gameState.isPlaying ? 'Restart' : 'Play'}
            </button>
          </div>
          
          {/* Message Display */}
          <div className="mt-4 text-center">
            <div className={`text-lg font-semibold ${
              gameState.message.includes('Correct') ? 'text-green-600' :
              gameState.message.includes('Wrong') ? 'text-red-600' :
              'text-blue-600'
            }`}>
              {gameState.message}
            </div>
          </div>
        </div>

        {/* Game Grid with Centered Target */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          {/* Centered Target Display */}
          <div className="text-center mb-6">
            <div className="inline-flex flex-col items-center">
              <Target className="w-12 h-12 text-blue-600 mb-2" />
              <div className="text-4xl font-bold text-gray-800">{gameState.target}</div>
              <div className="text-sm text-gray-600 mt-1">Target</div>
            </div>
          </div>

          {/* Game Grid */}
          <div className="grid grid-cols-10 gap-2 max-w-lg mx-auto">
            {gameState.grid.map((row, rowIndex) =>
              row.map((cell, colIndex) => (
                <button
                  key={`${rowIndex}-${colIndex}`}
                  onClick={() => handleCellClick(cell)}
                  className={`
                    w-12 h-12 rounded-lg border-2 font-bold text-lg transition-all duration-200
                    ${cell.isSelected 
                      ? 'bg-blue-500 text-white border-blue-600 scale-105' 
                      : 'bg-gray-50 text-gray-800 border-gray-200 hover:bg-gray-100'
                    }
                    ${!gameState.isPlaying ? 'opacity-50 cursor-not-allowed' : ''}
                  `}
                  disabled={!gameState.isPlaying}
                >
                  {cell.value}
                </button>
              ))
            )}
          </div>
        </div>

        {/* Instructions */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">How to Play:</h3>
          <ul className="text-gray-600 space-y-2">
            <li>• Select 3 numbers in a straight line (horizontal, vertical, or diagonal)</li>
            <li>• First two numbers multiply, third is added or subtracted</li>
            <li>• Result must equal the target number</li>
            <li><strong>Timed Mode:</strong> 300 seconds, score = number of correct guesses</li>
            <li><strong>Guesses Mode:</strong> 20 guesses, score = time to get 20 correct guesses</li>
            <li>• Incorrect guesses are immediately removed</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
