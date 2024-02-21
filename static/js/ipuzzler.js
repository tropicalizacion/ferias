class Puzzle {
  constructor(cells, clues, uri, hasSolution, submitUrl) {
    this.uri = uri || "";
    this.cells = cells;
    this.allCells.forEach((cell) => cell.puzzle = this);
    this.clues = clues;
    this.focusedCell = null;
    this.direction = "across";
    this.acrossHeading = "Across";
    this.downHeading = "Down";
    this.hasSolution = hasSolution;
    this.submitUrl = submitUrl != null ? submitUrl : "";
    console.log("SUBMIT" + this.submitUrl);
  }
  isClueBirectional(number) {
    return this.clues.across[number] && this.clues.down[number];
  }
  get allClues() {
    return this.clues.across.concat(this.clues.down).filter((clue) => clue);
  }
  get allCells() {
    return this.cells.flat();
  }
  switchDirection() {
    return this.direction == "across" ? this.direction = "down" : this.direction = "across";
  }
  get width() {
    return this.cells[0].length;
  }
  get height() {
    return this.cells.length;
  }
  get cookieName() {
    return this.uri.replace(/[^a-z0-9]+/ig, "-");
  }
  getState() {
    return this.cells.map((row) => row.map((cell) => cell.value || "_").join("")).join("");
  }
  setState(cookie) {
    let values = cookie.split("");
    let inputs = this.cells.flat();
    values.forEach((value, index) => inputs[index].setValue(value != "_" ? value : ""));
  }
  setFocus(row, col, toggleDirection) {
    this.setFocusToCell(this.cells[row][col], toggleDirection);
  }
  focusClue(clueNumber, clueDirection) {
    let clue = this.clues[clueDirection][clueNumber];
    this.setFocusToClue(clue);
  }
  setCellValue(value) {
    if (this.focusedCell) {
      this.focusedCell.setValue(value);
      if (value)
        this.advanceFocus(this.direction);
    }
  }
  setFocusToClue(clue) {
    this.direction = clue.direction;
    this.setFocusToCell(clue.cells[0]);
  }
  setFocusToCell(cell, toggleDirection) {
    if (cell && cell.hasInput) {
      if (this.focusedCell == cell) {
        if (cell.isBirectional && toggleDirection)
          this.switchDirection();
      } else {
        this.focusedCell = cell;
        if (!cell.clues[this.direction])
          this.switchDirection();
      }
      this.focusedCell = cell;
      this.focusedClue = cell.clues[this.direction];
      this.cells.flat().forEach((cell2) => cell2.clearHighlight());
      this.allClues.forEach((clue) => clue.clearHighlight());
      this.focusedClue.addHighlight();
    }
  }
  getCell(position) {
    if (position.isInside(this.cells))
      return this.cells[position.row][position.col];
    return null;
  }
  advanceFocus(direction) {
    let clue = this.focusedCell.clues[direction];
    let index = clue.cells.indexOf(this.focusedCell) + 1;
    if (index < clue.cells.length) {
      this.setFocusToCell(clue.cells[index]);
    } else if (clue.next) {
      this.setFocusToClue(clue.next);
    }
  }
  retreatFocus(direction) {
    let clue = this.focusedCell.clues[direction];
    if (clue) {
      let index = clue.cells.indexOf(this.focusedCell) - 1;
      if (index >= 0)
        this.setFocusToCell(clue.cells[index]);
    }
  }
  home() {
    this.setFocusToCell(this.focusedClue.cells[0]);
  }
  end() {
    this.setFocusToCell(this.focusedClue.cells[this.focusedClue.cells.length - 1]);
  }
  backspace() {
    this.setCellValue("");
    this.retreatFocus(this.direction);
  }
  clearFocus() {
    this.focusedCell = null;
    this.focusedClue = null;
    this.cells.flat().forEach((cell) => cell.clearHighlight());
    this.allClues.forEach((clue) => clue.clearHighlight());
  }
  moveFocus(direction) {
    var _a;
    let position = (_a = this.focusedCell) == null ? void 0 : _a.position;
    if (!position)
      return;
    let nextCell = this.getCell(position.increment(direction));
    this.setFocusToCell(nextCell);
  }
  checkClue() {
    if (this.focusedClue)
      this.focusedClue.check();
  }
  clearClue() {
    if (this.focusedClue)
      this.focusedClue.clear();
  }
  cheatClue() {
    if (this.focusedClue)
      this.focusedClue.cheat();
  }
  checkGrid() {
    this.allCells.forEach((cell) => cell.check());
  }
  clearGrid() {
    this.allCells.forEach((cell) => cell.clear());
  }
  cheatGrid() {
    this.allCells.forEach((cell) => cell.cheat());
  }
  submitGrid(form) {
    var decodedCookie = decodeURIComponent(document.cookie);
    var cookie = decodedCookie.split(/; */).map((token) => token.split("=")).find((pair) => pair[0] == this.cookieName);
    if (cookie && cookie.length > 1) {
      if (this.allCells.some((e) => e.style === "" && e.value === "")) {
        alert("You are missing some answers");
      } else {
        form.elements["answers"].value = cookie[1];
        form.submit();
      }
    }
  }
}
class Clue {
  constructor(ipuzClueData, direction) {
    this.direction = direction;
    this.number = parseInt(ipuzClueData.number);
    this.text = ipuzClueData.clue;
    this.enumeration = ipuzClueData.enumeration;
    this.label = (ipuzClueData.label || String(this.number)).replace(/\//g, ",").toLowerCase();
    this.cells = [];
    this.continuations = [];
    if (ipuzClueData.continued && ipuzClueData.continued.map) {
      this.continuations = ipuzClueData.continued.map((c) => {
        let continuation = new Clue(c, c.direction.toLowerCase());
        continuation.text = `See ${ipuzClueData.number}`;
        if (continuation.direction != this.direction)
          continuation.text += " " + this.direction;
        continuation.root = this;
        return continuation;
      });
      this.next = this.continuations[0];
      for (var i = 0; i < this.continuations.length - 1; i++)
        this.continuations[i].next = this.continuations[i + 1];
    }
  }
  get elementId() {
    return `clue-${this.number}-${this.direction}`;
  }
  get allCells() {
    var _a;
    let root = (_a = this.root) != null ? _a : this;
    return root.cells.concat(root.continuations.map((c) => c.cells).flat());
  }
  get allClues() {
    var _a;
    let root = (_a = this.root) != null ? _a : this;
    return [root].concat(root.continuations);
  }
  addHighlight() {
    this.allClues.forEach((clue) => clue.isActive = true);
    this.allCells.forEach((cell) => cell.addHighlight());
  }
  clearHighlight() {
    this.allClues.forEach((clue) => clue.isActive = false);
  }
  toClueList() {
    return [this].concat(this.continuations);
  }
  check() {
    this.allCells.forEach((cell) => cell.check());
  }
  clear() {
    this.allCells.forEach((cell) => cell.clear());
  }
  cheat() {
    this.allCells.forEach((cell) => cell.cheat());
  }
}
class Position {
  constructor(row, col) {
    this.row = row;
    this.col = col;
  }
  isInside(grid) {
    if (this.row < 0 || this.row >= grid.length)
      return false;
    if (this.col < 0 || this.col >= grid[this.row].length)
      return false;
    return true;
  }
  increment(direction) {
    switch (direction) {
      case "up":
        return new Position(this.row - 1, this.col);
      case "left":
        return new Position(this.row, this.col - 1);
      case "down":
        return new Position(this.row + 1, this.col);
      case "across":
      case "right":
        return new Position(this.row, this.col + 1);
    }
  }
}
class Cell {
  constructor(ipuzCellData, row, col) {
    this.isActive = false;
    this.style = "";
    this.position = new Position(row, col);
    this.previous = {};
    this.next = {};
    this.clues = {};
    this.value = "";
    if (ipuzCellData === null) {
      this.style = "blank";
    } else {
      if (typeof ipuzCellData.cell === "number") {
        this.number = ipuzCellData.cell;
      } else if (typeof ipuzCellData === "number") {
        this.number = ipuzCellData;
      } else {
        this.number = NaN;
      }
      if (ipuzCellData.style) {
        switch (ipuzCellData.style.barred) {
          case "T":
            this.style = "barred-top";
            break;
          case "L":
            this.style = "barred-left";
            break;
          case "TL":
            this.style = "barred-top barred-left";
            break;
        }
      } else if (ipuzCellData == "#") {
        this.style = "block";
      }
    }
  }
  setValue(value) {
    if (this.hasInput)
      this.value = value && value.toUpperCase ? value.toUpperCase() : "";
  }
  get isBirectional() {
    return this.clues["across"] && this.clues["down"];
  }
  get hasInput() {
    return !/bl(an|oc)k/.test(this.style);
  }
  addHighlight() {
    this.isActive = true;
  }
  clearHighlight() {
    this.isActive = false;
  }
  isEndOfRange(direction) {
    if (!this.hasInput)
      return true;
    if (direction == "across" && this.previous.across && /left/.test(this.style))
      return true;
    if (direction == "down" && this.previous.down && /top/.test(this.style))
      return true;
    return false;
  }
  check() {
    let value = this.value && this.value.toUpperCase ? this.value.toUpperCase() : "";
    let solution = this.solution && this.solution.toUpperCase ? this.solution.toUpperCase() : "";
    if (value !== solution)
      this.clear();
  }
  cheat() {
    if (this.solution)
      this.setValue(this.solution);
  }
  clear() {
    this.setValue("");
  }
}
class Parser {
  static parse(ipuzData, uri, submitUrl) {
    var _a, _b;
    let cells = ipuzData.puzzle.map((ipuzCells, row) => ipuzCells.map((ipuzCell, col) => new Cell(ipuzCell, row, col)));
    let hasSolution = Parser.attachSolutions(cells, ipuzData.solution);
    let clueKeys = Object.keys(ipuzData.clues);
    let acrossKey = clueKeys.find((key) => /^across/i.test(key));
    let downKey = clueKeys.find((key) => /^down/i.test(key));
    let acrossData = ipuzData.clues[acrossKey];
    let downData = ipuzData.clues[downKey];
    let cluesFromAcross = Array.isArray(acrossData) ? acrossData : [];
    cluesFromAcross = cluesFromAcross.map((c) => new Clue(c, "across").toClueList()).flat();
    let cluesFromDown = Array.isArray(downData) ? downData : [];
    cluesFromDown = cluesFromDown.map((c) => new Clue(c, "down").toClueList()).flat();
    const clues = { across: [], down: [] };
    cluesFromAcross.concat(cluesFromDown).forEach((clue) => {
      let cell = Parser.findCellForClue(cells, clue);
      if (cell) {
        clue.position = cell.position;
        clue.cells = Parser.findCellList(cells, clue.position, clue.direction);
        clue.cells.forEach((cell2) => cell2.clues[clue.direction] = clue);
        clues[clue.direction][clue.number] = clue;
      }
    });
    clues.across.heading = (_a = acrossKey.split(":")[1]) != null ? _a : "Across";
    clues.down.heading = (_b = downKey.split(":")[1]) != null ? _b : "Down";
    return new Puzzle(cells, clues, uri, hasSolution, submitUrl);
  }
  static attachSolutions(cells, solution) {
    if (!solution)
      return false;
    cells.forEach((line, row) => line.forEach((cell, col) => {
      if (solution[row] && solution[row][col]) {
        let value = solution[row][col].value || solution[row][col];
        if (value.toUpperCase && /[A-Z]/i.test(value))
          cell.solution = value.toUpperCase();
      }
    }));
    return true;
  }
  static findCellForClue(cells, clue) {
    return cells.flat().find((cell) => cell.number == clue.number);
  }
  static findCellList(cells, position, direction, previousCell) {
    if (!position.isInside(cells))
      return [];
    var cell = cells[position.row][position.col];
    cell.previous[direction] = previousCell;
    if (cell.isEndOfRange(direction))
      return [];
    if (previousCell)
      previousCell.next[direction] = cell;
    return [cell].concat(Parser.findCellList(cells, position.increment(direction), direction, cell));
  }
}
var styles = /* @__PURE__ */ (() => 'div.ipuzzler{font-family:Arial,Helvetica,sans-serif;font-size:12px;margin:0;padding:3px;display:grid;grid-template:1fr/auto 1fr 1fr}div.ipuzzler *{line-height:1em}@media only screen and (max-width: 640px){div.ipuzzler{display:block}}@media only screen and (max-width: 320px){div.ipuzzler div.puzzle-grid span span.clue-number{font-size:6px}}div.ipuzzler div#buttons{text-align:center}div.ipuzzler div#buttons button{margin:6px 4px 2px 0;width:6em;background-color:#36f;border:0;padding:4px;color:#fff;font-weight:400;border-radius:4px}div.ipuzzler div#buttons div#grid-buttons button{background-color:#809fff}div.ipuzzler div#buttons div#grid-buttons.no-solution,div.ipuzzler div#buttons div#clue-buttons.no-solution{display:inline}div.ipuzzler div#buttons div#clue-buttons.no-solution button{background-color:#809fff}div.ipuzzler div#buttons div#submit-buttons button{background-color:#36f;padding:6px;width:10em}div.ipuzzler div.clue-bar{display:none}@media only screen and (max-width: 640px){div.ipuzzler div.clue-bar{display:block}}div.ipuzzler div.clue-bar#above-clue-bar{margin-bottom:8px}div.ipuzzler div.clue-bar#below-clue-bar{margin:8px 0}div.ipuzzler div.clue-bar label{font-weight:700}div.ipuzzler div.clue-bar label:after{content:" "}div.ipuzzler div.clue-bar span:before{content:" "}div.ipuzzler div.puzzle-grid{background-color:#ff0;display:grid;background-color:#000;grid-gap:1px;border:1px solid #000;width:420px;height:420px;max-width:100%;box-sizing:border-box;grid-template:repeat(15,1fr)/repeat(15,1fr);margin:0}@media only screen and (max-width: 640px){div.ipuzzler div.puzzle-grid{width:calc(100vw - 10px);height:calc(100vw - 10px)}}@media only screen and (max-width: 320px){div.ipuzzler div.puzzle-grid{width:310px;height:310px}}div.ipuzzler div.puzzle-grid>span{background-color:#fff;text-align:center;position:relative}div.ipuzzler div.puzzle-grid>span label{font-size:8px;position:absolute;margin:0;padding:0;top:1px;left:1px;z-index:0;background:transparent}div.ipuzzler div.puzzle-grid>span.block{background-color:#000}div.ipuzzler div.puzzle-grid>span.blank{background-color:#933}div.ipuzzler div.puzzle-grid>span.barred-top{border-top:3px solid #000}div.ipuzzler div.puzzle-grid>span.barred-left{border-left:3px solid #000}div.ipuzzler div.puzzle-grid>span.highlighted{background-color:#9cf}div.ipuzzler div.puzzle-grid>span input{position:absolute;left:0;right:0;top:0;bottom:0;background-color:transparent;z-index:1;width:100%;height:100%;border:0;margin:0;padding:10% 0 0;font-weight:700;box-sizing:border-box;text-align:center;border-radius:0;-webkit-touch-callout:none;-webkit-user-select:none;user-select:none;mix-blend-mode:darken}div.ipuzzler div.puzzle-grid>span input:focus{font-weight:700;background-color:#36f!important;outline:2px solid #000}div.ipuzzler section.puzzle-clue-list{padding:0 8px}@media only screen and (max-width: 640px){div.ipuzzler section.puzzle-clue-list{padding:0}}div.ipuzzler section.puzzle-clue-list h2{font-size:100%;margin:0 0 8px}div.ipuzzler section.puzzle-clue-list ol{cursor:pointer;list-style:none;margin:0;padding:0}div.ipuzzler section.puzzle-clue-list ol li{padding:4px 4px 4px 1.8em;margin:0 0 2px;border-radius:4px;text-indent:-1.8em;line-height:1.2em}div.ipuzzler section.puzzle-clue-list ol li.highlighted{background-color:#9cf}div.ipuzzler section.puzzle-clue-list ol li.halflighted{background-color:#bdf}div.ipuzzler section.puzzle-clue-list ol li label{min-width:1.4em;font-weight:700;display:inline-block;text-indent:0;margin:0;padding:0 .3em 0 .1em}div.ipuzzler section.puzzle-clue-list ol li span:before{content:" "}\n')();
class Renderer {
  constructor(shadowDom) {
    this.dom = shadowDom;
    this.spans = [];
    this.inputs = [];
    this.labels = [];
    this.clueListItems = [];
    this.buttons = [];
    this.grid = null;
    this.aboveClueBar = null;
    this.belowClueBar = null;
  }
  html(tagName, attributes, innerText) {
    const element = document.createElement(tagName);
    for (const [key, value] of Object.entries(attributes || {}))
      element.setAttribute(key, value);
    if (innerText)
      element.innerText = innerText;
    return element;
  }
  update(puzzle) {
    this.spans.forEach((line, row) => line.forEach((span, col) => {
      let cell = puzzle.cells[row][col];
      if (cell == puzzle.focusedCell) {
        span.input.focus();
      } else if (span && span.input) {
        span.input.blur();
      }
      if (span.input)
        span.input.value = cell.value;
      if (cell.isActive) {
        span.classList.add("highlighted");
      } else {
        span.classList.remove("highlighted");
      }
    }));
    this.clueListItems.forEach((item) => {
      if (item.clue.isActive) {
        if (item.clue.root) {
          item.classList.add("halflighted");
        } else {
          item.classList.add("highlighted");
        }
      } else {
        item.classList.remove("highlighted");
        item.classList.remove("halflighted");
      }
    });
    if (puzzle.focusedClue) {
      this.drawClue(puzzle.focusedClue, this.aboveClueBar, true);
      this.drawClue(puzzle.focusedClue, this.belowClueBar, true);
    } else {
      this.aboveClueBar.innerHTML = "";
      this.belowClueBar.innerHTML = "";
    }
    this.savePuzzleStateToCookie(puzzle);
  }
  savePuzzleStateToCookie(puzzle) {
    var cookieValue = puzzle.getState();
    var cookieDate = new Date(2100, 1, 1);
    document.cookie = puzzle.cookieName + "=" + cookieValue + ";expires=" + cookieDate.toUTCString() + ";path=/";
  }
  loadPuzzleStateFromCookie(puzzle) {
    var cookies = decodeURIComponent(document.cookie).split(/; */);
    var cookie = cookies.map((c) => c.split("=")).find((pair) => pair[0] == puzzle.cookieName);
    if (cookie && cookie.length > 1)
      puzzle.setState(cookie[1]);
  }
  createCellSpan(cell, row, col) {
    let span = this.html("span");
    if (cell.style)
      span.className = cell.style;
    if (cell.number) {
      let label = this.html("label");
      label.innerHTML = cell.number;
      span.appendChild(label);
      this.labels.push(label);
    }
    if (cell.hasInput) {
      let clues = Object.entries(cell.clues).map((directionClues) => {
        const [direction, clue] = directionClues;
        return `clue-${clue.number}-${direction}`;
      });
      const attributes = { "data-row": row, "data-col": col, "value": cell.value };
      if (clues.length > 0) {
        attributes["aria-labelledby"] = clues.join(" ");
      }
      let input = this.html("input", attributes);
      span.appendChild(input);
      span.input = input;
      this.inputs.push(input);
    }
    return span;
  }
  createClueEnumerationSpan(clue) {
    const text = `${clue.enumeration.trim().replace(/ /g, ",")}`;
    let span = this.html("span", { "aria-label": `${text} characters.` });
    span.innerText = `(${text})`;
    return span;
  }
  createClueList(puzzle, direction) {
    let clues = puzzle.clues[direction.toLowerCase()];
    let id = `${direction.toLowerCase()}-clue-list`;
    let section = this.html("section", { "class": "puzzle-clue-list", "id": id });
    let heading = this.html("h2");
    heading.innerHTML = clues.heading;
    section.appendChild(heading);
    let list = this.html("ol");
    clues.forEach((clue) => {
      let item = this.html("li", { id: clue.elementId, "data-clue-number": clue.number, "data-clue-direction": clue.direction });
      this.drawClue(clue, item);
      item.clue = clue;
      this.clueListItems.push(item);
      list.appendChild(item);
    });
    section.appendChild(list);
    return section;
  }
  drawClue(clue, container, showDirection) {
    container.innerHTML = clue.text;
    let label = this.html("label", { "aria-label": `Direction ${clue.direction}:` });
    label.innerText = clue.label + (showDirection ? `${clue.direction[0]}` : "");
    container.insertBefore(label, container.firstChild);
    if (clue.enumeration)
      container.appendChild(this.createClueEnumerationSpan(clue));
  }
  drawButtons(hasSolution, submitUrl) {
    const checkClueButton = this.html("button", { "id": "check-clue-button" }, "Check clue");
    const clearClueButton = this.html("button", { "id": "clear-clue-button" }, "Clear clue");
    const cheatClueButton = this.html("button", { "id": "cheat-clue-button" }, "Cheat clue");
    const clueButtonContainer = hasSolution ? this.html("div", { "id": "clue-buttons" }) : this.html("div", { "id": "clue-buttons", "class": "no-solution" });
    const checkGridButton = this.html("button", { "id": "check-grid-button" }, "Check grid");
    const clearGridButton = this.html("button", { "id": "clear-grid-button" }, "Clear grid");
    const cheatGridButton = this.html("button", { "id": "cheat-grid-button" }, "Cheat grid");
    const gridButtonContainer = hasSolution ? this.html("div", { "id": "grid-buttons" }) : this.html("div", { "id": "grid-buttons", "class": "no-solution" });
    if (hasSolution) {
      clueButtonContainer.appendChild(checkClueButton);
      clueButtonContainer.appendChild(clearClueButton);
      clueButtonContainer.appendChild(cheatClueButton);
      gridButtonContainer.appendChild(checkGridButton);
      gridButtonContainer.appendChild(clearGridButton);
      gridButtonContainer.appendChild(cheatGridButton);
      this.buttons.push(checkClueButton);
      this.buttons.push(clearClueButton);
      this.buttons.push(cheatClueButton);
      this.buttons.push(checkGridButton);
      this.buttons.push(clearGridButton);
      this.buttons.push(cheatGridButton);
    } else {
      clueButtonContainer.appendChild(clearClueButton);
      gridButtonContainer.appendChild(clearGridButton);
      this.buttons.push(clearClueButton);
      this.buttons.push(clearGridButton);
    }
    const buttonBar = this.html("div", { "id": "buttons" });
    buttonBar.appendChild(clueButtonContainer);
    buttonBar.appendChild(gridButtonContainer);
    console.log("SUBMIT URL:" + submitUrl);
    if (submitUrl) {
      const submitButton = this.html("button", { "id": "submit-button", "type": "button" }, "Submit Answers");
      const submitButtonContainer = this.html("div", { "id": "submit-buttons" });
      const submitFormContainer = this.html("form", { "method": "POST", "action": submitUrl });
      const submitFormFieldContainer = this.html("input", { "type": "hidden", "id": "answers", "name": "answers" });
      submitButtonContainer.appendChild(submitButton);
      submitFormContainer.appendChild(submitButtonContainer);
      submitFormContainer.appendChild(submitFormFieldContainer);
      this.buttons.push(submitButton);
      buttonBar.appendChild(submitFormContainer);
    }
    return buttonBar;
  }
  render(puzzle) {
    this.loadPuzzleStateFromCookie(puzzle);
    const div = this.html("div", { "class": "ipuzzler" });
    this.dom.appendChild(div);
    const style = this.html("style");
    style.innerText = styles;
    div.appendChild(style);
    this.grid = this.html("div", { "class": "puzzle-grid" });
    this.grid.style.gridTemplate = `repeat(${puzzle.height}, 1fr) / repeat(${puzzle.width}, 1fr)`;
    let puzzleGridWrapper = this.html("div");
    this.aboveClueBar = this.html("div", { "class": "clue-bar", "id": "above-clue-bar" });
    this.belowClueBar = this.html("div", { "class": "clue-bar", "id": "below-clue-bar" });
    puzzleGridWrapper.appendChild(this.aboveClueBar);
    puzzleGridWrapper.appendChild(this.grid);
    puzzleGridWrapper.appendChild(this.belowClueBar);
    puzzleGridWrapper.appendChild(this.drawButtons(puzzle.hasSolution, puzzle.submitUrl));
    div.appendChild(puzzleGridWrapper);
    this.spans = puzzle.cells.map((row, rowIndex) => row.map((cell, colIndex) => {
      let span = this.createCellSpan(cell, rowIndex, colIndex);
      this.grid.appendChild(span);
      return span;
    }));
    div.appendChild(this.createClueList(puzzle, "Across"));
    div.appendChild(this.createClueList(puzzle, "Down"));
    this.resize(puzzle);
  }
  resize(puzzle) {
    let gridSize = Math.min(this.grid.offsetWidth, this.grid.offsetHeight);
    var inputFontSize = Math.ceil(gridSize / (1.8 * puzzle.width));
    if (inputFontSize > 10 && inputFontSize < 16)
      inputFontSize = 16;
    this.inputs.forEach((input) => input.style.fontSize = inputFontSize + "px");
    var labelFontSize = Math.ceil(gridSize / (4 * puzzle.width));
    this.labels.forEach((label) => label.style.fontSize = labelFontSize + "px");
    let windowWidth = Math.min(window.innerWidth, document.body.scrollWidth, document.body.clientWidth);
    let width, height;
    if (windowWidth > 768) {
      let cellSize = 28;
      width = puzzle.width * cellSize + puzzle.width + 1;
      height = puzzle.height * cellSize + puzzle.height + 1;
    } else {
      width = windowWidth - 10;
      height = Math.floor(puzzle.height / puzzle.width * width);
    }
    this.grid.style.width = width + "px";
    this.aboveClueBar.style.width = width + "px";
    this.belowClueBar.style.width = width + "px";
    this.grid.style.height = height + "px";
  }
}
class IPuzzler extends HTMLElement {
  constructor() {
    super();
    this.shadow = this.attachShadow({ mode: "open" });
    this.addEventListener("keydown", this.keydown);
    window.addEventListener("resize", this.resize.bind(this));
  }
  load(url, submitUrl) {
    fetch(url).then((response) => response.json()).then((json) => this.init(json, url, submitUrl));
  }
  init(json, url, submitUrl) {
    console.log(submitUrl);
    this.puzzle = Parser.parse(json, url, submitUrl);
    this.renderer = new Renderer(this.shadow);
    this.renderer.render(this.puzzle);
    this.renderer.inputs.forEach((input) => {
      input.addEventListener("focus", this.inputFocus.bind(this));
      input.addEventListener("mousedown", this.inputMouseDown.bind(this));
    });
    this.renderer.clueListItems.forEach((li) => li.addEventListener("click", this.clueListItemClick.bind(this)));
    this.renderer.buttons.forEach((button) => button.addEventListener("click", this.buttonClick.bind(this)));
    this.resize();
  }
  connectedCallback() {
    let url = this.getAttribute("src");
    let submitUrl = this.getAttribute("submitUrl");
    if (url)
      this.load(url, submitUrl);
  }
  attributeChangedCallback(name, oldValue, newValue) {
    let submitUrl = this.getAttribute("submitUrl");
    switch (name) {
      case "url":
        this.load(newValue, submitUrl);
        break;
    }
  }
  resize(event) {
    if (this.renderer && typeof this.renderer.resize == "function")
      this.renderer.resize(this.puzzle);
  }
  inputMouseDown(event) {
    let row = event.target.getAttribute("data-row");
    let col = event.target.getAttribute("data-col");
    this.puzzle.setFocus(row, col, true);
    this.renderer.update(this.puzzle);
  }
  inputFocus(event) {
    let row = event.target.getAttribute("data-row");
    let col = event.target.getAttribute("data-col");
    this.puzzle.setFocus(row, col);
    this.renderer.update(this.puzzle);
  }
  clueListItemClick(event) {
    let li = event.target.closest("li");
    let clueNumber = parseInt(li.getAttribute("data-clue-number"));
    let clueDirection = li.getAttribute("data-clue-direction");
    this.puzzle.focusClue(clueNumber, clueDirection);
    this.renderer.update(this.puzzle);
  }
  buttonClick(event) {
    let button = event.target;
    switch (button.id) {
      case "check-clue-button":
        this.puzzle.checkClue();
        break;
      case "clear-clue-button":
        this.puzzle.clearClue();
        break;
      case "cheat-clue-button":
        this.puzzle.cheatClue();
        break;
      case "check-grid-button":
        this.puzzle.checkGrid();
        break;
      case "clear-grid-button":
        this.puzzle.clearGrid();
        break;
      case "cheat-grid-button":
        if (confirm("Are you sure you want to reveal all solutions?"))
          this.puzzle.cheatGrid();
        break;
      case "submit-button":
        this.puzzle.submitGrid(button.closest("form"));
        break;
    }
    this.renderer.update(this.puzzle);
  }
  keydown(event) {
    if (event.ctrlKey || event.altKey || event.metaKey)
      return;
    let code = event.code;
    switch (code) {
      case "ArrowUp":
        this.puzzle.direction = "down";
        this.puzzle.moveFocus("up");
        break;
      case "ArrowDown":
        this.puzzle.direction = "down";
        this.puzzle.moveFocus("down");
        break;
      case "ArrowLeft":
        this.puzzle.direction = "across";
        this.puzzle.moveFocus("left");
        break;
      case "ArrowRight":
        this.puzzle.direction = "across";
        this.puzzle.moveFocus("right");
        break;
      case "Home":
        this.puzzle.home();
        break;
      case "End":
        this.puzzle.end();
        break;
      case "Backspace":
        this.puzzle.backspace();
        break;
      case "Delete":
        this.puzzle.setCellValue("");
        break;
      case "Escape":
        this.puzzle.clearFocus();
        break;
    }
    if (/^[a-z]$/i.test(event.key)) {
      this.puzzle.setCellValue(event.key);
      event.preventDefault();
    }
    this.renderer.update(this.puzzle);
  }
  static get observedAttributes() {
    return ["url"];
  }
}
customElements.define("ipuzzler-puzzle", IPuzzler);
export { IPuzzler };
