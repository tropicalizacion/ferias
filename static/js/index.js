import { newCrosswordController, helpers } from "../js/crosswords.js";

const { assert, eid, trace, tracing } = helpers;

// Load the initial crosswordSource (puzzle definition file).
// import crosswordDefinition from "../data/da_quick_20230818.json";
import crosswordDefinition from "../ftimes_17095.json";
// import crosswordDefinition from "../data/alberich_4.json";
// import crosswordDefinition from "../data/quiptic_89.json";
// import crosswordDefinition from "../data/bletchley_001.json";

// Enable console logging for crosswords-js
tracing(true);

// Check for browser context
assert(window && document, "Not in browser!");

// Locate the parent elements for the crossword-grid and crossword-clues DOM elements
const crosswordGridParent = eid("crossword-grid-placeholder");
const crosswordCluesParent = eid("crossword-clues-placeholder");

// Load _initial_ crossword file for demo.
loadController(crosswordDefinition, crosswordGridParent, crosswordCluesParent);

// Wire up crossword file picker
(function addCrosswordFileListener() {
  const cf = eid("crossword-file");
  cf.addEventListener("change", loadCrosswordPuzzle, false);
})();

// Crossword file picker "change" event handler
function loadCrosswordPuzzle(event) {
  // Nested helper executed when a file has been picked
  function reloadController(file) {
    const fr = new FileReader();
    // The onload event fires when the file has completed loading
    // The file content is in e.target.result
    fr.onload = (e) => {
      const fileText = e.target.result;
      // load new crossword into controller
      window.controller.loadCrosswordSource(file.type, fileText, file.name);
    };
    // Asynchronous
    fr.readAsText(file);
  }

  // Has a file been picked?
  if (this.files.length > 0) {
    // Yes!
    const puzzle = this.files[0];
    const [name, size, type] = [puzzle.name, puzzle.size, puzzle.type];
    trace(`loadCrosswordSource: ${name} (${size} B) type:"${type}"`);
    reloadController(puzzle);
  } else {
    // Nope
    trace(`loadCrosswordSource: cancelled`);
  }
}

// Helper function to create crossword controller
// and wire up page elements.
function loadController(
  crosswordDefinition,
  crosswordGridParent,
  crosswordCluesParent,
) {
  assert(
    crosswordDefinition,
    "[crosswordDefinition] argument is null or undefined",
  );
  // Entry point into package code...
  // Create the Controller and load the crossword grid
  // and clues view into the web page.
  const controller = newCrosswordController(
    crosswordDefinition,
    crosswordGridParent,
    crosswordCluesParent,
  );
  if (!controller?.isValid) {
    trace("loadController: Invalid [crosswordController].", "error");
    return false;
  }

  window.controller = controller;

  // Load title-block with initial crossword metadata
  loadTitleBlock(crosswordDefinition);

  //// Wire up all the Menu buttons

  // Bind all the Controller user-event handlers by their ids to the
  // click event of the matching DOM element (ids) in this example application.
  // Using default arguments:
  // elementIds = controller.userEventHandlerIds,
  // eventName = "click",
  // dom = document,
  controller.bindUserEventHandlersToIds();

  // Wire up handler for crosswordLoaded event
  addCrosswordLoadedListener(controller);
  // Wire up handler for clueSelected event
  addClueSelectedListener(controller);
  // Wire up handler for crosswordSolved event
  addCrosswordSolvedListener(controller, window);
  // Wire up handler for clueSolved event
  addClueSolvedListener(controller);
  // Wire up handler for clueIncomplete and crosswordIncomplete events
  addIncompleteListener(controller);

  return true;
}

// Wire up title block DOM elements
function addCrosswordLoadedListener(controller) {
  // Populate title block with crossword info
  const isou = eid("info-source-url");
  const iseu = eid("info-setter-url");

  controller.addEventsListener(["crosswordLoaded"], (crosswordDefinition) => {
    const cd = crosswordDefinition;
    isou.innerHTML = cd.source?.title;
    isou.setAttribute("href", cd.source?.url);
    iseu.innerHTML = cd.setter?.title;
    iseu.setAttribute("href", cd.setter?.url);
  });
}

// Wire up current-clue DOM elements
function addClueSelectedListener(controller) {
  const ccl = eid("current-clue-label");
  const cct = eid("current-clue-text");
  const cc = controller.currentClue;

  ccl.innerHTML = cc.labelText;
  cct.innerHTML = `${cc.clueText} ${cc.lengthText}`;
  // Update content of #current-clue when current clue changes
  controller.addEventsListener(["clueSelected"], (clue) => {
    ccl.innerHTML = clue.labelText;
    cct.innerHTML = `${clue.clueText} ${clue.lengthText}`;
  });
}

// Helper function to load TitleBlock DOM elements
// with initial crossword
function loadTitleBlock(crosswordDefinition) {
  // Populate title block with crossword info
  const iso = eid("info-source-url");
  const ise = eid("info-setter-url");
  const cd = crosswordDefinition;
  iso.innerHTML = cd.source?.title;
  iso.setAttribute("href", cd.source?.url);
  ise.innerHTML = cd.setter?.title;
  ise.setAttribute("href", cd.setter?.url);
}

// Respond to crosswordSolved event
function addCrosswordSolvedListener(controller, window) {
  // Locate element related to handler for CrosswordController "crosswordSolved" event
  const cso = eid("crossword-solved-overlay");

  controller.addEventsListener(["crosswordSolved"], (crosswordModel) => {
    trace("CrosswordSolvedHandler");
    // show the crossword-complete dialog
    cso.style.display = "block";
  });

  // Setup crossword completed display UI event handlers
  // eslint-disable-next-line no-param-reassign
  window.onclick = (event) => {
    // Hide the crossword-complete dialog When the user clicks anywhere.
    cso.style.display = "none";
    // Percolate the event
    return true;
  };
  // When the user types, close/hide it
  // eslint-disable-next-line no-param-reassign
  window.onkeydown = window.onclick;
}

// Respond to clueSolved event
function addClueSolvedListener(controller) {
  // Locate element related to handler for CrosswordController "clueSolved" event
  const csn = eid("clue-solved-notification");

  // show notification message and then fade out automatically
  // https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations/Tips
  controller.addEventsListener(["clueSolved"], (clue) => {
    trace("clueSolvedHandler");
    // Make notification visible - hidden initially.
    csn.style.display = "block";
    requestAnimationFrame((time) => {
      csn.className = "";
      requestAnimationFrame((time) => {
        csn.className = "fade-out";
      });
    });
  });
}

// Respond to Incomplete events
function addIncompleteListener(controller) {
  const icn = eid("incomplete-notification");

  // show notification message and then fade out automatically
  // https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations/Tips
  controller.addEventsListener(
    ["clueIncomplete", "crosswordIncomplete"],
    (arg) => {
      trace("incompleteHandler");
      // Make notification visible - hidden initially.
      icn.style.display = "block";
      requestAnimationFrame((time) => {
        icn.className = "";
        requestAnimationFrame((time) => {
          icn.className = "fade-out";
        });
      });
    },
  );
}
