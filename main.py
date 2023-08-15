<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Triozzle</title>
    <!-- linking to PyScript assets -->
    <link rel="stylesheet" href="https://pyscript.net/releases/2022.12.1/pyscript.css" />
    <script defer src="https://pyscript.net/releases/2022.12.1/pyscript.js"></script>
	<style>
		body {
			display: grid;
			place-items: center;
			height: 90vh;
			font-family: Arial, sans-serif;
			font-size: 100%;

		}

		#grid {
			display: none;
			Xborder: 3px solid green;
			height: 50vh;
			width: 50vh;
		}
		
		#startOverlay {
			height: 5vh;
			width: 50vh;
			justify-content: center;
			display: flex;
			Xborder: 3px solid brown;
		}
		
		.gamebartop {
			Xborder: 3px solid red;
			height: 5vh;
			width: 50vh;
			font-size: 1.5em;
			text-align: center;
		}
		
		.gamebarbottom {
			Xborder: 3px solid red;
			height: 5vh;
			width: 16vh;
			font-size: 1.5em;
			text-align: center;
		}
		
		.gamebartop_span {
			grid-template-columns: repeat(1, 1fr);
			grid-template-rows: repeat(2, 1fr);
			Xborder: 3px solid yellow;
			height: 11vh;
			width: 50vh;
			display: none;
			justify-content: center;
		}
		
		.gamebarbottom_span {
			grid-template-columns: repeat(3, 1fr);
			grid-template-rows: repeat(2, 1fr);
			Xborder: 3px solid yellow;
			height: 11vh;
			width: 50vh;
			display: none;
			justify-content: center;
		}
		
		.center-grid {
			justify-content: center;
		}

		.gridS {
			grid-template-columns: repeat(3, 1fr);
			grid-template-rows: repeat(3, 1fr);
		}
		
		.gridM {
			grid-template-columns: repeat(5, 1fr);
			grid-template-rows: repeat(5, 1fr);
		}
		
		.gridL {
			grid-template-columns: repeat(10, 1fr);
			grid-template-rows: repeat(10, 1fr);
			padding-top: 3px;
			gap: 3px;
			box-sizing: content-box;
		}
		
		.py-button {
			background: url('https://drive.google.com/uc?export=view&id=1gsEg-0xnadPcHTcEyBu6ZuIdpGpSXN5X') center/cover;
			background: url('https://drive.google.com/uc?export=view&id=1EUZO9zRg_1-6pZckV_LMm4LHnBReQ90G') center/cover;
			background: url('https://drive.google.com/uc?export=view&id=1Ojb3E0gNgMem0HbId-HsCY6VimlKjekE') center/cover;
			background: url('https://drive.google.com/uc?export=view&id=1QONmorajfvvFmFi1LQlXHlcMwWSPURzb') center/cover;
			background: url('https://drive.google.com/uc?export=view&id=1HtSlekxn-g7nsYy2MDbXXHzGDYmCwFiW') center/cover;
			color: white;
			text-align: center;
			font-size: 1.5em;
			cursor: pointer;
			height: 100%;
			width: 100%;
			border: none;
		}

		.btn_shown {
			display: grid;
		}
		
		.btn_hidden {
			display: none;
		}
		
		.btn_result {
			Xborder: 3px solid blue;
		}
		
		.btn_chosen {
			Xborder: 3px solid red;
			background: url('https://drive.google.com/uc?export=view&id=1QONmorajfvvFmFi1LQlXHlcMwWSPURzb') center/cover;
			background-repeat:no-repeat
		}

		.btn_error {
			background: url('https://drive.google.com/uc?export=view&id=1EUZO9zRg_1-6pZckV_LMm4LHnBReQ90G') center/cover;
			background-repeat:no-repeat
		}

		.timer {
			background: url('https://drive.google.com/uc?export=view&id=1QONmorajfvvFmFi1LQlXHlcMwWSPURzb') center/cover;
			background-repeat:no-repeat;
		}
		
		.result {
			background: url('https://drive.google.com/uc?export=view&id=1gsEg-0xnadPcHTcEyBu6ZuIdpGpSXN5X') center/cover;
			background-repeat:no-repeat;
			color: black;
		}
		
		.errors {
			background: url('https://drive.google.com/uc?export=view&id=1EUZO9zRg_1-6pZckV_LMm4LHnBReQ90G') center/cover;
			background-repeat:no-repeat;
		}
		
		.round {
			background: url('https://drive.google.com/uc?export=view&id=1Ojb3E0gNgMem0HbId-HsCY6VimlKjekE') center/cover;
			background-repeat:no-repeat;
		}
		
		.overlay {
		  height: 100vh;
		  width: 0;
		  position: fixed;
		  z-index: 1;
		  top: 0;
		  left: 0;
		  background-color: rgb(12,100,73);
		  background-color: rgba(12,100,73, 0.9);
		  overflow-x: hidden;
		  transition: 0.5s;
		}

		.overlay-content {
		  position: relative;
		  top: 5%;
		  width: 100%;
		  text-align: center;
		  margin-top: 30px;
		}

		.overlay p {
		  padding: 8px;
		  text-decoration: none;
		  font-size: 1.5em;
		  color: #f1f1f1;
		  display: block;
		  transition: 0.3s;
		}

		.overlay p:hover, .overlay p:focus {
		  color: #f1f1f1;
		}

		@media screen and (max-height: 450px) {
		  .overlay p {font-size: 1.5em}
		}
	</style>
  </head>
  <body>
	<div id="endOverlay" class="overlay">
	  <div class="overlay-content">
		<p id="endTitle">X</p>
		<img id="star" src="https://drive.google.com/uc?export=view&id=18rP3iDqwSYCsDlbN1_Wu4PemTmXpV7Gz" alt="star" width="150" height="150">
		<p id="endScore">0</p>
		<p id="endTimes">0</p>
		<p id="endDateTime"></p>
		<p id="nextgameDateTime"></p>
	  </div>
	</div>
	<div id="main" class="center-grid">
		<div id="startOverlay">
			<span>
				<div>
					<button id="start" py-click="start_game('daily')" class="py-button">Daily Challenge</button>
					<p align="center"> ... OR ...</p>
					<button id="practice" py-click="start_game('practice')" class="py-button btn_error">Practice</button>
				</div>
				<br>
				<p><b>How to play Triozzle:</b>
				<br>Solve for the result shown in the yellow box at the top.
				<br>You're given a 10x10 grid filled with numbers from 0 to 9.
				<br>Click 3 numbers in the grid that are in a line (left, right, up, down or diagonally) that make up the result when the first 2 numbers are multiplied and the 3rd number is either subtracted or added from their product: (A x B) +/- C = Result
				<br>(e.g. 5 * 2 - 1 = 9 or 7 * 6 + 6 = 48)
				<br>
				<br>You play for 10 rounds, with each round having a new grid and result.
				<br>Be quick... your score depends on how quickly you solve for the result.
				<br>But, you only can have 3 incorrect guesses before your game is over.
				<br>
				<br><b>Tips:</b>
				<li>You can deselect a number by clicking it again</li>
				<li>There is only 1 Triozzle Daily Challenge per day</li>
<!--				<li>You can only play once per day. New puzzles appear at the start of the day (UTC time) -->
				</p>
			</span>
		</div>
		<div id="gamebartop" class="gamebartop_span">
			<span id="game_resultTxt" class="gamebartop">Result</span>
			<button id="game_result" class="py-button result gamebartop">??</button>
		</div>
		<div id="grid" class="gridL">
			<button id="btn10" py-click="btn_click(10)" class="py-button">?</button>
			<button id="btn11" py-click="btn_click(11)" class="py-button">?</button>
			<button id="btn12" py-click="btn_click(12)" class="py-button">?</button>
			<button id="btn13" py-click="btn_click(13)" class="py-button">?</button>
			<button id="btn14" py-click="btn_click(14)" class="py-button">?</button>
			<button id="btn15" py-click="btn_click(15)" class="py-button">?</button>
			<button id="btn16" py-click="btn_click(16)" class="py-button">?</button>
			<button id="btn17" py-click="btn_click(17)" class="py-button">?</button>
			<button id="btn18" py-click="btn_click(18)" class="py-button">?</button>
			<button id="btn19" py-click="btn_click(19)" class="py-button">?</button>
			<button id="btn20" py-click="btn_click(20)" class="py-button">?</button>
			<button id="btn21" py-click="btn_click(21)" class="py-button">?</button>
			<button id="btn22" py-click="btn_click(22)" class="py-button">?</button>
			<button id="btn23" py-click="btn_click(23)" class="py-button">?</button>
			<button id="btn24" py-click="btn_click(24)" class="py-button">?</button>
			<button id="btn25" py-click="btn_click(25)" class="py-button">?</button>
			<button id="btn26" py-click="btn_click(26)" class="py-button">?</button>
			<button id="btn27" py-click="btn_click(27)" class="py-button">?</button>
			<button id="btn28" py-click="btn_click(28)" class="py-button">?</button>
			<button id="btn29" py-click="btn_click(29)" class="py-button">?</button>
			<button id="btn30" py-click="btn_click(30)" class="py-button">?</button>
			<button id="btn31" py-click="btn_click(31)" class="py-button">?</button>
			<button id="btn32" py-click="btn_click(32)" class="py-button">?</button>
			<button id="btn33" py-click="btn_click(33)" class="py-button">?</button>
			<button id="btn34" py-click="btn_click(34)" class="py-button">?</button>
			<button id="btn35" py-click="btn_click(35)" class="py-button">?</button>
			<button id="btn36" py-click="btn_click(36)" class="py-button">?</button>
			<button id="btn37" py-click="btn_click(37)" class="py-button">?</button>
			<button id="btn38" py-click="btn_click(38)" class="py-button">?</button>
			<button id="btn39" py-click="btn_click(39)" class="py-button">?</button>
			<button id="btn40" py-click="btn_click(40)" class="py-button">?</button>
			<button id="btn41" py-click="btn_click(41)" class="py-button">?</button>
			<button id="btn42" py-click="btn_click(42)" class="py-button">?</button>
			<button id="btn43" py-click="btn_click(43)" class="py-button">?</button>
			<button id="btn44" py-click="btn_click(44)" class="py-button">?</button>
			<button id="btn45" py-click="btn_click(45)" class="py-button">?</button>
			<button id="btn46" py-click="btn_click(46)" class="py-button">?</button>
			<button id="btn47" py-click="btn_click(47)" class="py-button">?</button>
			<button id="btn48" py-click="btn_click(48)" class="py-button">?</button>
			<button id="btn49" py-click="btn_click(49)" class="py-button">?</button>
			<button id="btn50" py-click="btn_click(50)" class="py-button">?</button>
			<button id="btn51" py-click="btn_click(51)" class="py-button">?</button>
			<button id="btn52" py-click="btn_click(52)" class="py-button">?</button>
			<button id="btn53" py-click="btn_click(53)" class="py-button">?</button>
			<button id="btn54" py-click="btn_click(54)" class="py-button">?</button>
			<button id="btn55" py-click="btn_click(55)" class="py-button">?</button>
			<button id="btn56" py-click="btn_click(56)" class="py-button">?</button>
			<button id="btn57" py-click="btn_click(57)" class="py-button">?</button>
			<button id="btn58" py-click="btn_click(58)" class="py-button">?</button>
			<button id="btn59" py-click="btn_click(59)" class="py-button">?</button>
			<button id="btn60" py-click="btn_click(60)" class="py-button">?</button>
			<button id="btn61" py-click="btn_click(61)" class="py-button">?</button>
			<button id="btn62" py-click="btn_click(62)" class="py-button">?</button>
			<button id="btn63" py-click="btn_click(63)" class="py-button">?</button>
			<button id="btn64" py-click="btn_click(64)" class="py-button">?</button>
			<button id="btn65" py-click="btn_click(65)" class="py-button">?</button>
			<button id="btn66" py-click="btn_click(66)" class="py-button">?</button>
			<button id="btn67" py-click="btn_click(67)" class="py-button">?</button>
			<button id="btn68" py-click="btn_click(68)" class="py-button">?</button>
			<button id="btn69" py-click="btn_click(69)" class="py-button">?</button>
			<button id="btn70" py-click="btn_click(70)" class="py-button">?</button>
			<button id="btn71" py-click="btn_click(71)" class="py-button">?</button>
			<button id="btn72" py-click="btn_click(72)" class="py-button">?</button>
			<button id="btn73" py-click="btn_click(73)" class="py-button">?</button>
			<button id="btn74" py-click="btn_click(74)" class="py-button">?</button>
			<button id="btn75" py-click="btn_click(75)" class="py-button">?</button>
			<button id="btn76" py-click="btn_click(76)" class="py-button">?</button>
			<button id="btn77" py-click="btn_click(77)" class="py-button">?</button>
			<button id="btn78" py-click="btn_click(78)" class="py-button">?</button>
			<button id="btn79" py-click="btn_click(79)" class="py-button">?</button>
			<button id="btn80" py-click="btn_click(80)" class="py-button">?</button>
			<button id="btn81" py-click="btn_click(81)" class="py-button">?</button>
			<button id="btn82" py-click="btn_click(82)" class="py-button">?</button>
			<button id="btn83" py-click="btn_click(83)" class="py-button">?</button>
			<button id="btn84" py-click="btn_click(84)" class="py-button">?</button>
			<button id="btn85" py-click="btn_click(85)" class="py-button">?</button>
			<button id="btn86" py-click="btn_click(86)" class="py-button">?</button>
			<button id="btn87" py-click="btn_click(87)" class="py-button">?</button>
			<button id="btn88" py-click="btn_click(88)" class="py-button">?</button>
			<button id="btn89" py-click="btn_click(89)" class="py-button">?</button>
			<button id="btn90" py-click="btn_click(90)" class="py-button">?</button>
			<button id="btn91" py-click="btn_click(91)" class="py-button">?</button>
			<button id="btn92" py-click="btn_click(92)" class="py-button">?</button>
			<button id="btn93" py-click="btn_click(93)" class="py-button">?</button>
			<button id="btn94" py-click="btn_click(94)" class="py-button">?</button>
			<button id="btn95" py-click="btn_click(95)" class="py-button">?</button>
			<button id="btn96" py-click="btn_click(96)" class="py-button">?</button>
			<button id="btn97" py-click="btn_click(97)" class="py-button">?</button>
			<button id="btn98" py-click="btn_click(98)" class="py-button">?</button>
			<button id="btn99" py-click="btn_click(99)" class="py-button">?</button>
			<button id="btn100" py-click="btn_click(100)" class="py-button">?</button>
			<button id="btn101" py-click="btn_click(101)" class="py-button">?</button>
			<button id="btn102" py-click="btn_click(102)" class="py-button">?</button>
			<button id="btn103" py-click="btn_click(103)" class="py-button">?</button>
			<button id="btn104" py-click="btn_click(104)" class="py-button">?</button>
			<button id="btn105" py-click="btn_click(105)" class="py-button">?</button>
			<button id="btn106" py-click="btn_click(106)" class="py-button">?</button>
			<button id="btn107" py-click="btn_click(107)" class="py-button">?</button>
			<button id="btn108" py-click="btn_click(108)" class="py-button">?</button>
			<button id="btn109" py-click="btn_click(109)" class="py-button">?</button>
		</div>
		<div id="gamebarbottom" class="gamebarbottom_span">
			<span id="timerTxt" class="gamebarbottom">Timer</span>
			<span id="curr_roundTxt" class="gamebarbottom">Round</span>
			<span id="num_of_errorsTxt" class="gamebarbottom">Errors</span>
			<button id="timer" class="py-button timer gamebarbottom">0</button>
			<button id="curr_round" class="py-button round gamebarbottom">0</button>
			<button id="num_of_errors" class="py-button errors gamebarbottom">0</button>
		</div>
	</div>
  <!-- Put Python code inside the the <py-script> tag -->
    <py-config>
		packages = ['numpy']
		terminal = false
		[[fetch]]
		from = "https://raw.githubusercontent.com/elyders/triozzle/main/"
		files = ["main.py"]
	</py-config>
	<py-script src="https://raw.githubusercontent.com/elyders/triozzle/main/main.py"></py-script>
  </body>
</html>
