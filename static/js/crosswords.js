var Kr = Object.defineProperty;
var Vr = (e, n, r) => n in e ? Kr(e, n, { enumerable: !0, configurable: !0, writable: !0, value: r }) : e[n] = r;
var j = (e, n, r) => (Vr(e, typeof n != "symbol" ? n + "" : n, r), r), Ve = (e, n, r) => {
  if (!n.has(e))
    throw TypeError("Cannot " + r);
};
var p = (e, n, r) => (Ve(e, n, "read from private field"), r ? r.call(e) : n.get(e)), v = (e, n, r) => {
  if (n.has(e))
    throw TypeError("Cannot add the same private member more than once");
  n instanceof WeakSet ? n.add(e) : n.set(e, r);
}, D = (e, n, r, i) => (Ve(e, n, "write to private field"), i ? i.call(e, r) : n.set(e, r), r);
var E = (e, n, r) => (Ve(e, n, "access private method"), r);
function I(e, n) {
  e.classList.add(n);
}
function Le(e, n) {
  n.forEach((r) => {
    e.classList.add(r);
  });
}
function d(e, n) {
  if (!e)
    throw new Error(n || "Assertion failed");
}
const On = (e, n = document) => n.getElementById(e), Nn = (e, n = document) => n.getElementsByClassName(e);
function qr(e, n, r) {
  let i = e;
  if (e && n != null && r) {
    let l = parseInt(n, 10);
    l < 0 && (l = e.length + l), l >= 0 && e.length > l && (i = `${e.slice(0, l)}${r}${e.slice(
      l + r.length
    )}`);
  }
  return i;
}
function ke(e, n) {
  e.classList.remove(n);
}
function oe(e, n, r) {
  let i = e ?? "";
  return i = i.padEnd(n + 1, " "), qr(i, n, r);
}
let $n = !1;
const Gr = (e) => {
  $n = e;
}, x = (e, n = "log") => {
  $n && (d(
    ["log", "warn", "error"].includes(n),
    `Unsupported action'${n}'.`
  ), console[n](e));
}, Wr = () => {
  const e = {}, n = e.hasOwnProperty;
  return {
    publish: (r, i) => {
      n.call(e, r) && e[r].forEach((l) => {
        l(i !== void 0 ? i : {});
      });
    },
    subscribe: (r, i) => {
      n.call(e, r) || (e[r] = []);
      const l = e[r].push(i) - 1;
      return {
        remove: () => {
          delete e[r][l];
        }
      };
    }
  };
};
var V;
class dn {
  constructor() {
    /** @type {Record<string, any>} */
    v(this, V, {});
    /**
     * Gets the DOM element for a modelCell.
     * @param {*} modelCell
     * @returns {HTMLDivElement}
     */
    j(this, "cellElement", (n) => (d(typeof n == "object", "Cell is not an object"), n.cellElement));
    //  Gets the modelCell for a DOM element.
    j(this, "modelCell", (n) => {
      switch (typeof n) {
        case "string":
          return p(this, V)[n];
        case "object":
          return p(this, V)[n.dataset.xy];
        default:
          d(!0, 'Unexpected type for "cellElement"');
          break;
      }
    });
  }
  /**
   * Adds a Cell <-> Cell Element mapping.
   * @param {*} modelCell
   * @param {HTMLDivElement} cellElement
   */
  add(n, r) {
    d(n, "modelCell is null or undefined"), d(r, "cellElement is null or undefined"), p(this, V)[r.dataset.xy] = n;
  }
  get modelCells() {
    return Object.values(p(this, V));
  }
}
V = new WeakMap();
function Qr(e, n) {
  x("newCrosswordCluesView"), d(e, "[document] is null or undefined"), d(n, "[controller] is null or undefined"), d(n.model, "[controller.model] is null or undefined");
  function r(o, u) {
    let s = e.createElement("div");
    I(s, "crossword-clue-block"), s.id = o;
    let c = e.createElement("p");
    return c.innerHTML = u, I(c, "crossword-clue-block-title"), s.appendChild(c), s;
  }
  function i(o, u, s) {
    s.forEach((c) => {
      let f = e.createElement("div");
      I(f, "crossword-clue"), f.modelClue = c;
      let a = e.createElement("span");
      I(a, "crossword-clue-label"), a.innerHTML = `${c.labelText}`, f.appendChild(a);
      let m = e.createElement("span");
      I(m, "crossword-clue-text"), m.innerHTML = `${c.clueText} ${c.lengthText}`, f.appendChild(m), f.addEventListener("click", (g) => {
        x(`clue(${c.labelText}):click`), o.lastMoveEvent = "click", o.currentClue = c;
      }), u.appendChild(f);
    });
  }
  function l(o) {
    const u = n.currentClue;
    if (o === u)
      return !0;
    {
      const s = u.headSegment;
      return s === o || s.tailSegments.indexOf(o) !== -1;
    }
  }
  let t = {
    wrapper: e.createElement("div"),
    acrossClues: r("crossword-across-clues", "Across"),
    downClues: r("crossword-down-clues", "Down")
  };
  return Le(t.wrapper, ["crosswords-js", "crossword-clues"]), i(n, t.acrossClues, n.model.acrossClues), t.wrapper.appendChild(t.acrossClues), i(n, t.downClues, n.model.downClues), t.wrapper.appendChild(t.downClues), n.addEventsListener(["clueSelected"], (o) => {
    for (const u of t.acrossClues.children)
      l(u.modelClue) ? I(u, "current-clue-segment") : ke(u, "current-clue-segment");
    for (const u of t.downClues.children)
      l(u.modelClue) ? I(u, "current-clue-segment") : ke(u, "current-clue-segment");
  }), t.wrapper;
}
function zr(e, n, r) {
  x("newCrosswordGridView"), d(
    e,
    "DOM root element [document] argument is null or undefined."
  ), d(n, "CrosswordModel [model] argument is null or undefined."), d(
    r,
    "CrosswordController [cellMap] argument is null or undefined."
  );
  let i = e.createElement("div");
  Le(i, ["crosswords-js", "crossword-grid"]), i.style.setProperty("--row-count", n.height), i.style.setProperty("--column-count", n.width);
  for (let l = 0; l < n.height; l += 1)
    for (let t = 0; t < n.width; t += 1) {
      const o = n.cells[t][l], u = Xr(e, o);
      r.add(o, u), i.appendChild(u);
    }
  return i;
}
function Xr(e, n) {
  let r = e.createElement("div");
  if (r.dataset.xy = n, I(r, "cwcell"), n.cellElement = r, I(r, n.light ? "light" : "dark"), !n.light)
    return r;
  if (r.tabIndex = 0, I(r, "noselect"), r.appendChild(new Text(n.answer ?? " ")), n.labelText) {
    const t = e.createElement("div");
    I(t, "cwclue-label"), t.innerHTML = n.labelText, r.appendChild(t);
  }
  const i = e.createElement("div");
  Le(i, ["cwcell-revealed", "hidden"]), r.appendChild(i);
  const l = e.createElement("div");
  return Le(l, ["cwcell-incorrect", "hidden"]), r.appendChild(l), n.acrossTerminator && I(r, "cw-across-word-separator"), n.downTerminator && I(r, "cw-down-word-separator"), r;
}
function Rn(e, n) {
  const [r, i, l] = [
    n,
    e,
    n.acrossClue && n.downClue
  ];
  return l && (x("toggleClueDirection"), i.currentClue = r.acrossClue === i.currentClue ? r.downClue : r.acrossClue), l;
}
function Dn(e, n) {
  const [r, , i] = [
    n,
    e,
    e.currentClue
  ], o = (r.acrossClue === i ? r.acrossClueLetterIndex : r.downClueLetterIndex) + 1 === i.cells.length && i.nextClueSegment;
  return o && (cc.currentClue = i.nextClueSegment), o;
}
function Mn(e, n) {
  const [r, i] = [n, e], l = i.currentClue, u = (r.acrossClue === l ? r.acrossClueLetterIndex : r.downClueLetterIndex) - 1 === -1 && l.previousClueSegment;
  return u && (i.currentCell = l.previousClueSegment.cells.slice(-1)[0], i.currentClue = l.previousClueSegment), u;
}
function Bn(e, n) {
  const { x: r, y: i } = n, { height: l } = n.model;
  let t = !1;
  return n.y + 1 < l && n.model.cells[r][i + 1].light === !0 ? (e.currentCell = n.model.cells[r][i + 1], t = !0) : t = Dn(e, n), t;
}
function Hn(e, n) {
  const { x: r, y: i } = n, { width: l } = n.model;
  let t = !1;
  return n.x + 1 < l && n.model.cells[r + 1][i].light === !0 ? (e.currentCell = n.model.cells[r + 1][i], t = !0) : t = Dn(e, n), t;
}
function jn(e, n) {
  const { x: r, y: i } = n;
  let l = !1;
  return n.y > 0 && n.model.cells[r][i - 1].light === !0 ? (e.currentCell = n.model.cells[r][i - 1], l = !0) : l = Mn(e, n), l;
}
function Pn(e, n) {
  const { x: r, y: i } = n;
  let l = !1;
  return n.x > 0 && n.model.cells[r - 1][i].light === !0 ? (e.currentCell = n.model.cells[r - 1][i], l = !0) : l = Mn(e, n), l;
}
function Un(e, n) {
  if (e.currentClue === n.acrossClue)
    return Hn(e, n);
  if (e.currentClue === n.downClue)
    return Bn(e, n);
}
function hn(e, n) {
  if (e.currentClue === n.acrossClue)
    return Pn(e, n);
  if (e.currentClue === n.downClue)
    return jn(e, n);
}
const Yn = (e, n) => n.isAcross ? [
  e.acrossClues.headSegments,
  e.downClues.headSegments
] : [
  e.downClues.headSegments,
  e.acrossClues.headSegments
];
function Zr(e, n) {
  const r = e.currentClue.headSegment, [i, l] = Yn(n.model, r), t = i.indexOf(r);
  d(t !== -1, `clue '${r.clueId}' not found in headClues`), e.currentClue = t === i.length - 1 ? (
    // current head is last - flip direction, get first head clue
    l[0]
  ) : (
    // get next head
    i[t + 1]
  );
}
function Jr(e, n) {
  const r = e.currentClue.headSegment, [i, l] = Yn(n.model, r), t = i.indexOf(r);
  d(t !== -1, `clue '${r.clueId}' not found in headClues`), e.currentClue = t === 0 ? (
    // current head is first - flip direction, get last head clue
    l.slice(-1)[0]
  ) : (
    // get previous head
    i[t - 1]
  );
}
function pn(e, n, r) {
  Kn(e, n, " "), ue(e.incorrectElement(r));
}
function Kn(e, n, r) {
  const i = e.cell(n.target);
  n.target.firstChild.nodeValue = r, i.acrossClue && (i.acrossClue.answer = oe(
    i.acrossClue.answer,
    i.acrossClueLetterIndex,
    r
  )), i.downClue && (i.downClue.answer = oe(
    i.downClue.answer,
    i.downClueLetterIndex,
    r
  ));
}
const ue = (e) => {
  e == null || e.classList.add("hidden");
}, Vn = (e) => {
  e == null || e.classList.remove("hidden");
};
function ei(e, n, r) {
  d(n, "newClue is undefined"), r == null || r.headSegment.flatCells.forEach((i) => {
    ke(e.cellElement(i), "active");
  }), n.headSegment.flatCells.forEach((i) => {
    I(e.cellElement(i), "active");
  });
}
function ni(e, n, r) {
  d(n, "newCell is undefined"), r && ke(e.cellElement(r), "highlighted"), I(e.cellElement(n), "highlighted");
}
const M = Object.freeze({
  backspace: "Backspace",
  delete: "Delete",
  down: "ArrowDown",
  enter: "Enter",
  left: "ArrowLeft",
  right: "ArrowRight",
  space: " ",
  tab: "Tab",
  up: "ArrowUp",
  shift: "Shift",
  alt: "Alt",
  ctrl: "Control",
  name: (e) => {
    const n = Object.entries(M).find(
      (r) => r[1] === e
    );
    return n ? n[0] : null;
  }
});
function rn(e, n) {
  var o;
  d(e, "<controller> is null or undefined"), d(n, "<cell> is null or undefined");
  const r = n.acrossClue ? n.acrossClue : n.downClue, i = n.acrossClue ? n.acrossClueLetterIndex : n.downClueLetterIndex, l = i < ((o = r.solution) == null ? void 0 : o.length) ? r.solution[i] : " ";
  Ye(e, n, l, !1), Vn(e.revealedElement(n)), ue(e.incorrectElement(n));
}
function ri(e, n) {
  d(e, "<controller> is null or undefined"), d(n, "<clue> is null or undefined"), x(`revealClue: '${n}'`), n.headSegment.flatCells.forEach((r) => {
    rn(e, r);
  });
}
function ii(e) {
  d(e, "<controller> is null or undefined"), e.model.lightCells.forEach((n) => {
    rn(e, n);
  });
}
const _ = Object.freeze({
  correct: 0,
  // 0 elements empty, N elements correct
  incorrect: 1,
  // 1+ elements incorrect
  incomplete: 2
  // 1+ elements empty, 0 elements incorrect
});
function Pe(e, n) {
  return e ? _.incorrect : n ? _.incomplete : _.correct;
}
function Ue(e, n, r = !0) {
  d(e, "<controller> is null or undefined"), d(n, "<cell> is null or undefined");
  const [i, l] = n.acrossClue ? [n.acrossClue, n.acrossClueLetterIndex] : [n.downClue, n.downClueLetterIndex], t = i.answer[l], o = i.solution ? i.solution[l] : void 0, u = Pe(
    !(t === o || t === " "),
    t === " " || t === void 0
  );
  return u === _.incorrect && r && Vn(e.incorrectElement(n)), u;
}
function li(e, n, r = !0) {
  d(e, "<controller> is null or undefined"), d(n, "<clue> is null or undefined"), x(`testClue: '${n}'`);
  let i = 0, l = 0;
  return n.headSegment.flatCells.forEach((t) => {
    const o = Ue(e, t, r);
    o === _.incorrect ? i += 1 : o === _.incomplete && (l += 1);
  }), Pe(i > 0, l > 0);
}
function ti(e, n = !0) {
  d(e, "<controller> is null or undefined");
  let r = 0, i = 0;
  return e.model.lightCells.forEach((l) => {
    const t = Ue(e, l, n);
    t === _.incorrect ? r += 1 : t === _.incomplete && (i += 1);
  }), Pe(r > 0, i > 0);
}
function oi(e) {
  d(e, "<controller> is null or undefined");
  let n = 0, r = 0;
  const i = !1;
  return e.model.lightCells.find((l) => {
    const t = Ue(e, l, i);
    if (t === _.incorrect)
      return n += 1, !0;
    if (t === _.incomplete)
      return r += 1, !0;
  }), Pe(n > 0, r > 0);
}
function Ye(e, n, r, i = !0) {
  d(e, "<controller> is null or undefined"), d(
    (n == null ? void 0 : n.acrossClue) || (n == null ? void 0 : n.downClue),
    "cell is null or not part of a clue"
  ), d((r == null ? void 0 : r.length) === 1, "newText must be a single character");
  function l(t, o) {
    let u = t;
    u.answer = oe(u.answer, o, r), i && (u.revealed = oe(u.revealed, o, r));
  }
  if (n.acrossClue) {
    let t = n.acrossClue;
    const o = n.acrossClueLetterIndex;
    l(t, o);
  }
  if (n.downClue) {
    let t = n.downClue;
    const o = n.downClueLetterIndex;
    l(t, o);
  }
  e.setCellElementText(n, r);
}
function qn(e, n, r = !1) {
  d(e, "<controller> is null or undefined"), d(n, "<cell> is null or undefined"), Ye(e, n, " "), ue(e.incorrectElement(n)), r && ue(e.revealedElement(n));
}
function ui(e, n) {
  d(e, "<controller> is null or undefined"), d(n, "<clue> is null or undefined"), x(`resetClue: '${n}'`), n.headSegment.flatCells.forEach((r) => {
    qn(e, r);
  });
}
function si(e) {
  d(e, "<controller> is null or undefined"), e.model.lightCells.forEach((n) => {
    qn(e, n, !0);
  });
}
function Gn(e, n) {
  d(e, "<controller> is null or undefined"), d(n, "<cell> is null or undefined");
  const r = Ue(e, n) === _.incorrect;
  r && (Ye(e, n, " ", r), ue(e.incorrectElement(n)));
}
function ci(e, n) {
  d(e, "<controller> is null or undefined"), d(n, "<clue> is null or undefined"), x(`cleanClue: '${n}'`), n.headSegment.flatCells.forEach((r) => {
    Gn(e, r);
  });
}
function ai(e) {
  x("cleanCrossword"), d(e, "<controller> is null or undefined"), e.model.lightCells.forEach((n) => {
    Gn(e, n);
  });
}
/*! js-yaml 4.1.0 https://github.com/nodeca/js-yaml @license MIT */
function Wn(e) {
  return typeof e > "u" || e === null;
}
function fi(e) {
  return typeof e == "object" && e !== null;
}
function di(e) {
  return Array.isArray(e) ? e : Wn(e) ? [] : [e];
}
function hi(e, n) {
  var r, i, l, t;
  if (n)
    for (t = Object.keys(n), r = 0, i = t.length; r < i; r += 1)
      l = t[r], e[l] = n[l];
  return e;
}
function pi(e, n) {
  var r = "", i;
  for (i = 0; i < n; i += 1)
    r += e;
  return r;
}
function mi(e) {
  return e === 0 && Number.NEGATIVE_INFINITY === 1 / e;
}
var gi = Wn, xi = fi, Ci = di, wi = pi, vi = mi, yi = hi, S = {
  isNothing: gi,
  isObject: xi,
  toArray: Ci,
  repeat: wi,
  isNegativeZero: vi,
  extend: yi
};
function Qn(e, n) {
  var r = "", i = e.reason || "(unknown reason)";
  return e.mark ? (e.mark.name && (r += 'in "' + e.mark.name + '" '), r += "(" + (e.mark.line + 1) + ":" + (e.mark.column + 1) + ")", !n && e.mark.snippet && (r += `

` + e.mark.snippet), i + " " + r) : i;
}
function de(e, n) {
  Error.call(this), this.name = "YAMLException", this.reason = e, this.mark = n, this.message = Qn(this, !1), Error.captureStackTrace ? Error.captureStackTrace(this, this.constructor) : this.stack = new Error().stack || "";
}
de.prototype = Object.create(Error.prototype);
de.prototype.constructor = de;
de.prototype.toString = function(n) {
  return this.name + ": " + Qn(this, n);
};
var F = de;
function qe(e, n, r, i, l) {
  var t = "", o = "", u = Math.floor(l / 2) - 1;
  return i - n > u && (t = " ... ", n = i - u + t.length), r - i > u && (o = " ...", r = i + u - o.length), {
    str: t + e.slice(n, r).replace(/\t/g, "→") + o,
    pos: i - n + t.length
    // relative position
  };
}
function Ge(e, n) {
  return S.repeat(" ", n - e.length) + e;
}
function Ei(e, n) {
  if (n = Object.create(n || null), !e.buffer)
    return null;
  n.maxLength || (n.maxLength = 79), typeof n.indent != "number" && (n.indent = 1), typeof n.linesBefore != "number" && (n.linesBefore = 3), typeof n.linesAfter != "number" && (n.linesAfter = 2);
  for (var r = /\r?\n|\r|\0/g, i = [0], l = [], t, o = -1; t = r.exec(e.buffer); )
    l.push(t.index), i.push(t.index + t[0].length), e.position <= t.index && o < 0 && (o = i.length - 2);
  o < 0 && (o = i.length - 1);
  var u = "", s, c, f = Math.min(e.line + n.linesAfter, l.length).toString().length, a = n.maxLength - (n.indent + f + 3);
  for (s = 1; s <= n.linesBefore && !(o - s < 0); s++)
    c = qe(
      e.buffer,
      i[o - s],
      l[o - s],
      e.position - (i[o] - i[o - s]),
      a
    ), u = S.repeat(" ", n.indent) + Ge((e.line - s + 1).toString(), f) + " | " + c.str + `
` + u;
  for (c = qe(e.buffer, i[o], l[o], e.position, a), u += S.repeat(" ", n.indent) + Ge((e.line + 1).toString(), f) + " | " + c.str + `
`, u += S.repeat("-", n.indent + f + 3 + c.pos) + `^
`, s = 1; s <= n.linesAfter && !(o + s >= l.length); s++)
    c = qe(
      e.buffer,
      i[o + s],
      l[o + s],
      e.position - (i[o] - i[o + s]),
      a
    ), u += S.repeat(" ", n.indent) + Ge((e.line + s + 1).toString(), f) + " | " + c.str + `
`;
  return u.replace(/\n$/, "");
}
var Ai = Ei, bi = [
  "kind",
  "multi",
  "resolve",
  "construct",
  "instanceOf",
  "predicate",
  "represent",
  "representName",
  "defaultStyle",
  "styleAliases"
], Si = [
  "scalar",
  "sequence",
  "mapping"
];
function Ti(e) {
  var n = {};
  return e !== null && Object.keys(e).forEach(function(r) {
    e[r].forEach(function(i) {
      n[String(i)] = r;
    });
  }), n;
}
function _i(e, n) {
  if (n = n || {}, Object.keys(n).forEach(function(r) {
    if (bi.indexOf(r) === -1)
      throw new F('Unknown option "' + r + '" is met in definition of "' + e + '" YAML type.');
  }), this.options = n, this.tag = e, this.kind = n.kind || null, this.resolve = n.resolve || function() {
    return !0;
  }, this.construct = n.construct || function(r) {
    return r;
  }, this.instanceOf = n.instanceOf || null, this.predicate = n.predicate || null, this.represent = n.represent || null, this.representName = n.representName || null, this.defaultStyle = n.defaultStyle || null, this.multi = n.multi || !1, this.styleAliases = Ti(n.styleAliases || null), Si.indexOf(this.kind) === -1)
    throw new F('Unknown kind "' + this.kind + '" is specified for "' + e + '" YAML type.');
}
var T = _i;
function mn(e, n) {
  var r = [];
  return e[n].forEach(function(i) {
    var l = r.length;
    r.forEach(function(t, o) {
      t.tag === i.tag && t.kind === i.kind && t.multi === i.multi && (l = o);
    }), r[l] = i;
  }), r;
}
function Li() {
  var e = {
    scalar: {},
    sequence: {},
    mapping: {},
    fallback: {},
    multi: {
      scalar: [],
      sequence: [],
      mapping: [],
      fallback: []
    }
  }, n, r;
  function i(l) {
    l.multi ? (e.multi[l.kind].push(l), e.multi.fallback.push(l)) : e[l.kind][l.tag] = e.fallback[l.tag] = l;
  }
  for (n = 0, r = arguments.length; n < r; n += 1)
    arguments[n].forEach(i);
  return e;
}
function Qe(e) {
  return this.extend(e);
}
Qe.prototype.extend = function(n) {
  var r = [], i = [];
  if (n instanceof T)
    i.push(n);
  else if (Array.isArray(n))
    i = i.concat(n);
  else if (n && (Array.isArray(n.implicit) || Array.isArray(n.explicit)))
    n.implicit && (r = r.concat(n.implicit)), n.explicit && (i = i.concat(n.explicit));
  else
    throw new F("Schema.extend argument should be a Type, [ Type ], or a schema definition ({ implicit: [...], explicit: [...] })");
  r.forEach(function(t) {
    if (!(t instanceof T))
      throw new F("Specified list of YAML types (or a single Type object) contains a non-Type object.");
    if (t.loadKind && t.loadKind !== "scalar")
      throw new F("There is a non-scalar type in the implicit list of a schema. Implicit resolving of such types is not supported.");
    if (t.multi)
      throw new F("There is a multi type in the implicit list of a schema. Multi tags can only be listed as explicit.");
  }), i.forEach(function(t) {
    if (!(t instanceof T))
      throw new F("Specified list of YAML types (or a single Type object) contains a non-Type object.");
  });
  var l = Object.create(Qe.prototype);
  return l.implicit = (this.implicit || []).concat(r), l.explicit = (this.explicit || []).concat(i), l.compiledImplicit = mn(l, "implicit"), l.compiledExplicit = mn(l, "explicit"), l.compiledTypeMap = Li(l.compiledImplicit, l.compiledExplicit), l;
};
var zn = Qe, Xn = new T("tag:yaml.org,2002:str", {
  kind: "scalar",
  construct: function(e) {
    return e !== null ? e : "";
  }
}), Zn = new T("tag:yaml.org,2002:seq", {
  kind: "sequence",
  construct: function(e) {
    return e !== null ? e : [];
  }
}), Jn = new T("tag:yaml.org,2002:map", {
  kind: "mapping",
  construct: function(e) {
    return e !== null ? e : {};
  }
}), er = new zn({
  explicit: [
    Xn,
    Zn,
    Jn
  ]
});
function ki(e) {
  if (e === null)
    return !0;
  var n = e.length;
  return n === 1 && e === "~" || n === 4 && (e === "null" || e === "Null" || e === "NULL");
}
function Ii() {
  return null;
}
function Fi(e) {
  return e === null;
}
var nr = new T("tag:yaml.org,2002:null", {
  kind: "scalar",
  resolve: ki,
  construct: Ii,
  predicate: Fi,
  represent: {
    canonical: function() {
      return "~";
    },
    lowercase: function() {
      return "null";
    },
    uppercase: function() {
      return "NULL";
    },
    camelcase: function() {
      return "Null";
    },
    empty: function() {
      return "";
    }
  },
  defaultStyle: "lowercase"
});
function Oi(e) {
  if (e === null)
    return !1;
  var n = e.length;
  return n === 4 && (e === "true" || e === "True" || e === "TRUE") || n === 5 && (e === "false" || e === "False" || e === "FALSE");
}
function Ni(e) {
  return e === "true" || e === "True" || e === "TRUE";
}
function $i(e) {
  return Object.prototype.toString.call(e) === "[object Boolean]";
}
var rr = new T("tag:yaml.org,2002:bool", {
  kind: "scalar",
  resolve: Oi,
  construct: Ni,
  predicate: $i,
  represent: {
    lowercase: function(e) {
      return e ? "true" : "false";
    },
    uppercase: function(e) {
      return e ? "TRUE" : "FALSE";
    },
    camelcase: function(e) {
      return e ? "True" : "False";
    }
  },
  defaultStyle: "lowercase"
});
function Ri(e) {
  return 48 <= e && e <= 57 || 65 <= e && e <= 70 || 97 <= e && e <= 102;
}
function Di(e) {
  return 48 <= e && e <= 55;
}
function Mi(e) {
  return 48 <= e && e <= 57;
}
function Bi(e) {
  if (e === null)
    return !1;
  var n = e.length, r = 0, i = !1, l;
  if (!n)
    return !1;
  if (l = e[r], (l === "-" || l === "+") && (l = e[++r]), l === "0") {
    if (r + 1 === n)
      return !0;
    if (l = e[++r], l === "b") {
      for (r++; r < n; r++)
        if (l = e[r], l !== "_") {
          if (l !== "0" && l !== "1")
            return !1;
          i = !0;
        }
      return i && l !== "_";
    }
    if (l === "x") {
      for (r++; r < n; r++)
        if (l = e[r], l !== "_") {
          if (!Ri(e.charCodeAt(r)))
            return !1;
          i = !0;
        }
      return i && l !== "_";
    }
    if (l === "o") {
      for (r++; r < n; r++)
        if (l = e[r], l !== "_") {
          if (!Di(e.charCodeAt(r)))
            return !1;
          i = !0;
        }
      return i && l !== "_";
    }
  }
  if (l === "_")
    return !1;
  for (; r < n; r++)
    if (l = e[r], l !== "_") {
      if (!Mi(e.charCodeAt(r)))
        return !1;
      i = !0;
    }
  return !(!i || l === "_");
}
function Hi(e) {
  var n = e, r = 1, i;
  if (n.indexOf("_") !== -1 && (n = n.replace(/_/g, "")), i = n[0], (i === "-" || i === "+") && (i === "-" && (r = -1), n = n.slice(1), i = n[0]), n === "0")
    return 0;
  if (i === "0") {
    if (n[1] === "b")
      return r * parseInt(n.slice(2), 2);
    if (n[1] === "x")
      return r * parseInt(n.slice(2), 16);
    if (n[1] === "o")
      return r * parseInt(n.slice(2), 8);
  }
  return r * parseInt(n, 10);
}
function ji(e) {
  return Object.prototype.toString.call(e) === "[object Number]" && e % 1 === 0 && !S.isNegativeZero(e);
}
var ir = new T("tag:yaml.org,2002:int", {
  kind: "scalar",
  resolve: Bi,
  construct: Hi,
  predicate: ji,
  represent: {
    binary: function(e) {
      return e >= 0 ? "0b" + e.toString(2) : "-0b" + e.toString(2).slice(1);
    },
    octal: function(e) {
      return e >= 0 ? "0o" + e.toString(8) : "-0o" + e.toString(8).slice(1);
    },
    decimal: function(e) {
      return e.toString(10);
    },
    /* eslint-disable max-len */
    hexadecimal: function(e) {
      return e >= 0 ? "0x" + e.toString(16).toUpperCase() : "-0x" + e.toString(16).toUpperCase().slice(1);
    }
  },
  defaultStyle: "decimal",
  styleAliases: {
    binary: [2, "bin"],
    octal: [8, "oct"],
    decimal: [10, "dec"],
    hexadecimal: [16, "hex"]
  }
}), Pi = new RegExp(
  // 2.5e4, 2.5 and integers
  "^(?:[-+]?(?:[0-9][0-9_]*)(?:\\.[0-9_]*)?(?:[eE][-+]?[0-9]+)?|\\.[0-9_]+(?:[eE][-+]?[0-9]+)?|[-+]?\\.(?:inf|Inf|INF)|\\.(?:nan|NaN|NAN))$"
);
function Ui(e) {
  return !(e === null || !Pi.test(e) || // Quick hack to not allow integers end with `_`
  // Probably should update regexp & check speed
  e[e.length - 1] === "_");
}
function Yi(e) {
  var n, r;
  return n = e.replace(/_/g, "").toLowerCase(), r = n[0] === "-" ? -1 : 1, "+-".indexOf(n[0]) >= 0 && (n = n.slice(1)), n === ".inf" ? r === 1 ? Number.POSITIVE_INFINITY : Number.NEGATIVE_INFINITY : n === ".nan" ? NaN : r * parseFloat(n, 10);
}
var Ki = /^[-+]?[0-9]+e/;
function Vi(e, n) {
  var r;
  if (isNaN(e))
    switch (n) {
      case "lowercase":
        return ".nan";
      case "uppercase":
        return ".NAN";
      case "camelcase":
        return ".NaN";
    }
  else if (Number.POSITIVE_INFINITY === e)
    switch (n) {
      case "lowercase":
        return ".inf";
      case "uppercase":
        return ".INF";
      case "camelcase":
        return ".Inf";
    }
  else if (Number.NEGATIVE_INFINITY === e)
    switch (n) {
      case "lowercase":
        return "-.inf";
      case "uppercase":
        return "-.INF";
      case "camelcase":
        return "-.Inf";
    }
  else if (S.isNegativeZero(e))
    return "-0.0";
  return r = e.toString(10), Ki.test(r) ? r.replace("e", ".e") : r;
}
function qi(e) {
  return Object.prototype.toString.call(e) === "[object Number]" && (e % 1 !== 0 || S.isNegativeZero(e));
}
var lr = new T("tag:yaml.org,2002:float", {
  kind: "scalar",
  resolve: Ui,
  construct: Yi,
  predicate: qi,
  represent: Vi,
  defaultStyle: "lowercase"
}), tr = er.extend({
  implicit: [
    nr,
    rr,
    ir,
    lr
  ]
}), or = tr, ur = new RegExp(
  "^([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])$"
), sr = new RegExp(
  "^([0-9][0-9][0-9][0-9])-([0-9][0-9]?)-([0-9][0-9]?)(?:[Tt]|[ \\t]+)([0-9][0-9]?):([0-9][0-9]):([0-9][0-9])(?:\\.([0-9]*))?(?:[ \\t]*(Z|([-+])([0-9][0-9]?)(?::([0-9][0-9]))?))?$"
);
function Gi(e) {
  return e === null ? !1 : ur.exec(e) !== null || sr.exec(e) !== null;
}
function Wi(e) {
  var n, r, i, l, t, o, u, s = 0, c = null, f, a, m;
  if (n = ur.exec(e), n === null && (n = sr.exec(e)), n === null)
    throw new Error("Date resolve error");
  if (r = +n[1], i = +n[2] - 1, l = +n[3], !n[4])
    return new Date(Date.UTC(r, i, l));
  if (t = +n[4], o = +n[5], u = +n[6], n[7]) {
    for (s = n[7].slice(0, 3); s.length < 3; )
      s += "0";
    s = +s;
  }
  return n[9] && (f = +n[10], a = +(n[11] || 0), c = (f * 60 + a) * 6e4, n[9] === "-" && (c = -c)), m = new Date(Date.UTC(r, i, l, t, o, u, s)), c && m.setTime(m.getTime() - c), m;
}
function Qi(e) {
  return e.toISOString();
}
var cr = new T("tag:yaml.org,2002:timestamp", {
  kind: "scalar",
  resolve: Gi,
  construct: Wi,
  instanceOf: Date,
  represent: Qi
});
function zi(e) {
  return e === "<<" || e === null;
}
var ar = new T("tag:yaml.org,2002:merge", {
  kind: "scalar",
  resolve: zi
}), ln = `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=
\r`;
function Xi(e) {
  if (e === null)
    return !1;
  var n, r, i = 0, l = e.length, t = ln;
  for (r = 0; r < l; r++)
    if (n = t.indexOf(e.charAt(r)), !(n > 64)) {
      if (n < 0)
        return !1;
      i += 6;
    }
  return i % 8 === 0;
}
function Zi(e) {
  var n, r, i = e.replace(/[\r\n=]/g, ""), l = i.length, t = ln, o = 0, u = [];
  for (n = 0; n < l; n++)
    n % 4 === 0 && n && (u.push(o >> 16 & 255), u.push(o >> 8 & 255), u.push(o & 255)), o = o << 6 | t.indexOf(i.charAt(n));
  return r = l % 4 * 6, r === 0 ? (u.push(o >> 16 & 255), u.push(o >> 8 & 255), u.push(o & 255)) : r === 18 ? (u.push(o >> 10 & 255), u.push(o >> 2 & 255)) : r === 12 && u.push(o >> 4 & 255), new Uint8Array(u);
}
function Ji(e) {
  var n = "", r = 0, i, l, t = e.length, o = ln;
  for (i = 0; i < t; i++)
    i % 3 === 0 && i && (n += o[r >> 18 & 63], n += o[r >> 12 & 63], n += o[r >> 6 & 63], n += o[r & 63]), r = (r << 8) + e[i];
  return l = t % 3, l === 0 ? (n += o[r >> 18 & 63], n += o[r >> 12 & 63], n += o[r >> 6 & 63], n += o[r & 63]) : l === 2 ? (n += o[r >> 10 & 63], n += o[r >> 4 & 63], n += o[r << 2 & 63], n += o[64]) : l === 1 && (n += o[r >> 2 & 63], n += o[r << 4 & 63], n += o[64], n += o[64]), n;
}
function el(e) {
  return Object.prototype.toString.call(e) === "[object Uint8Array]";
}
var fr = new T("tag:yaml.org,2002:binary", {
  kind: "scalar",
  resolve: Xi,
  construct: Zi,
  predicate: el,
  represent: Ji
}), nl = Object.prototype.hasOwnProperty, rl = Object.prototype.toString;
function il(e) {
  if (e === null)
    return !0;
  var n = [], r, i, l, t, o, u = e;
  for (r = 0, i = u.length; r < i; r += 1) {
    if (l = u[r], o = !1, rl.call(l) !== "[object Object]")
      return !1;
    for (t in l)
      if (nl.call(l, t))
        if (!o)
          o = !0;
        else
          return !1;
    if (!o)
      return !1;
    if (n.indexOf(t) === -1)
      n.push(t);
    else
      return !1;
  }
  return !0;
}
function ll(e) {
  return e !== null ? e : [];
}
var dr = new T("tag:yaml.org,2002:omap", {
  kind: "sequence",
  resolve: il,
  construct: ll
}), tl = Object.prototype.toString;
function ol(e) {
  if (e === null)
    return !0;
  var n, r, i, l, t, o = e;
  for (t = new Array(o.length), n = 0, r = o.length; n < r; n += 1) {
    if (i = o[n], tl.call(i) !== "[object Object]" || (l = Object.keys(i), l.length !== 1))
      return !1;
    t[n] = [l[0], i[l[0]]];
  }
  return !0;
}
function ul(e) {
  if (e === null)
    return [];
  var n, r, i, l, t, o = e;
  for (t = new Array(o.length), n = 0, r = o.length; n < r; n += 1)
    i = o[n], l = Object.keys(i), t[n] = [l[0], i[l[0]]];
  return t;
}
var hr = new T("tag:yaml.org,2002:pairs", {
  kind: "sequence",
  resolve: ol,
  construct: ul
}), sl = Object.prototype.hasOwnProperty;
function cl(e) {
  if (e === null)
    return !0;
  var n, r = e;
  for (n in r)
    if (sl.call(r, n) && r[n] !== null)
      return !1;
  return !0;
}
function al(e) {
  return e !== null ? e : {};
}
var pr = new T("tag:yaml.org,2002:set", {
  kind: "mapping",
  resolve: cl,
  construct: al
}), tn = or.extend({
  implicit: [
    cr,
    ar
  ],
  explicit: [
    fr,
    dr,
    hr,
    pr
  ]
}), K = Object.prototype.hasOwnProperty, Ie = 1, mr = 2, gr = 3, Fe = 4, We = 1, fl = 2, gn = 3, dl = /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x84\x86-\x9F\uFFFE\uFFFF]|[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?:[^\uD800-\uDBFF]|^)[\uDC00-\uDFFF]/, hl = /[\x85\u2028\u2029]/, pl = /[,\[\]\{\}]/, xr = /^(?:!|!!|![a-z\-]+!)$/i, Cr = /^(?:!|[^,\[\]\{\}])(?:%[0-9a-f]{2}|[0-9a-z\-#;\/\?:@&=\+\$,_\.!~\*'\(\)\[\]])*$/i;
function xn(e) {
  return Object.prototype.toString.call(e);
}
function B(e) {
  return e === 10 || e === 13;
}
function z(e) {
  return e === 9 || e === 32;
}
function O(e) {
  return e === 9 || e === 32 || e === 10 || e === 13;
}
function ne(e) {
  return e === 44 || e === 91 || e === 93 || e === 123 || e === 125;
}
function ml(e) {
  var n;
  return 48 <= e && e <= 57 ? e - 48 : (n = e | 32, 97 <= n && n <= 102 ? n - 97 + 10 : -1);
}
function gl(e) {
  return e === 120 ? 2 : e === 117 ? 4 : e === 85 ? 8 : 0;
}
function xl(e) {
  return 48 <= e && e <= 57 ? e - 48 : -1;
}
function Cn(e) {
  return e === 48 ? "\0" : e === 97 ? "\x07" : e === 98 ? "\b" : e === 116 || e === 9 ? "	" : e === 110 ? `
` : e === 118 ? "\v" : e === 102 ? "\f" : e === 114 ? "\r" : e === 101 ? "\x1B" : e === 32 ? " " : e === 34 ? '"' : e === 47 ? "/" : e === 92 ? "\\" : e === 78 ? "" : e === 95 ? " " : e === 76 ? "\u2028" : e === 80 ? "\u2029" : "";
}
function Cl(e) {
  return e <= 65535 ? String.fromCharCode(e) : String.fromCharCode(
    (e - 65536 >> 10) + 55296,
    (e - 65536 & 1023) + 56320
  );
}
var wr = new Array(256), vr = new Array(256);
for (var Z = 0; Z < 256; Z++)
  wr[Z] = Cn(Z) ? 1 : 0, vr[Z] = Cn(Z);
function wl(e, n) {
  this.input = e, this.filename = n.filename || null, this.schema = n.schema || tn, this.onWarning = n.onWarning || null, this.legacy = n.legacy || !1, this.json = n.json || !1, this.listener = n.listener || null, this.implicitTypes = this.schema.compiledImplicit, this.typeMap = this.schema.compiledTypeMap, this.length = e.length, this.position = 0, this.line = 0, this.lineStart = 0, this.lineIndent = 0, this.firstTabInLine = -1, this.documents = [];
}
function yr(e, n) {
  var r = {
    name: e.filename,
    buffer: e.input.slice(0, -1),
    // omit trailing \0
    position: e.position,
    line: e.line,
    column: e.position - e.lineStart
  };
  return r.snippet = Ai(r), new F(n, r);
}
function h(e, n) {
  throw yr(e, n);
}
function Oe(e, n) {
  e.onWarning && e.onWarning.call(null, yr(e, n));
}
var wn = {
  YAML: function(n, r, i) {
    var l, t, o;
    n.version !== null && h(n, "duplication of %YAML directive"), i.length !== 1 && h(n, "YAML directive accepts exactly one argument"), l = /^([0-9]+)\.([0-9]+)$/.exec(i[0]), l === null && h(n, "ill-formed argument of the YAML directive"), t = parseInt(l[1], 10), o = parseInt(l[2], 10), t !== 1 && h(n, "unacceptable YAML version of the document"), n.version = i[0], n.checkLineBreaks = o < 2, o !== 1 && o !== 2 && Oe(n, "unsupported YAML version of the document");
  },
  TAG: function(n, r, i) {
    var l, t;
    i.length !== 2 && h(n, "TAG directive accepts exactly two arguments"), l = i[0], t = i[1], xr.test(l) || h(n, "ill-formed tag handle (first argument) of the TAG directive"), K.call(n.tagMap, l) && h(n, 'there is a previously declared suffix for "' + l + '" tag handle'), Cr.test(t) || h(n, "ill-formed tag prefix (second argument) of the TAG directive");
    try {
      t = decodeURIComponent(t);
    } catch {
      h(n, "tag prefix is malformed: " + t);
    }
    n.tagMap[l] = t;
  }
};
function Y(e, n, r, i) {
  var l, t, o, u;
  if (n < r) {
    if (u = e.input.slice(n, r), i)
      for (l = 0, t = u.length; l < t; l += 1)
        o = u.charCodeAt(l), o === 9 || 32 <= o && o <= 1114111 || h(e, "expected valid JSON character");
    else
      dl.test(u) && h(e, "the stream contains non-printable characters");
    e.result += u;
  }
}
function vn(e, n, r, i) {
  var l, t, o, u;
  for (S.isObject(r) || h(e, "cannot merge mappings; the provided source object is unacceptable"), l = Object.keys(r), o = 0, u = l.length; o < u; o += 1)
    t = l[o], K.call(n, t) || (n[t] = r[t], i[t] = !0);
}
function re(e, n, r, i, l, t, o, u, s) {
  var c, f;
  if (Array.isArray(l))
    for (l = Array.prototype.slice.call(l), c = 0, f = l.length; c < f; c += 1)
      Array.isArray(l[c]) && h(e, "nested arrays are not supported inside keys"), typeof l == "object" && xn(l[c]) === "[object Object]" && (l[c] = "[object Object]");
  if (typeof l == "object" && xn(l) === "[object Object]" && (l = "[object Object]"), l = String(l), n === null && (n = {}), i === "tag:yaml.org,2002:merge")
    if (Array.isArray(t))
      for (c = 0, f = t.length; c < f; c += 1)
        vn(e, n, t[c], r);
    else
      vn(e, n, t, r);
  else
    !e.json && !K.call(r, l) && K.call(n, l) && (e.line = o || e.line, e.lineStart = u || e.lineStart, e.position = s || e.position, h(e, "duplicated mapping key")), l === "__proto__" ? Object.defineProperty(n, l, {
      configurable: !0,
      enumerable: !0,
      writable: !0,
      value: t
    }) : n[l] = t, delete r[l];
  return n;
}
function on(e) {
  var n;
  n = e.input.charCodeAt(e.position), n === 10 ? e.position++ : n === 13 ? (e.position++, e.input.charCodeAt(e.position) === 10 && e.position++) : h(e, "a line break is expected"), e.line += 1, e.lineStart = e.position, e.firstTabInLine = -1;
}
function b(e, n, r) {
  for (var i = 0, l = e.input.charCodeAt(e.position); l !== 0; ) {
    for (; z(l); )
      l === 9 && e.firstTabInLine === -1 && (e.firstTabInLine = e.position), l = e.input.charCodeAt(++e.position);
    if (n && l === 35)
      do
        l = e.input.charCodeAt(++e.position);
      while (l !== 10 && l !== 13 && l !== 0);
    if (B(l))
      for (on(e), l = e.input.charCodeAt(e.position), i++, e.lineIndent = 0; l === 32; )
        e.lineIndent++, l = e.input.charCodeAt(++e.position);
    else
      break;
  }
  return r !== -1 && i !== 0 && e.lineIndent < r && Oe(e, "deficient indentation"), i;
}
function Ke(e) {
  var n = e.position, r;
  return r = e.input.charCodeAt(n), !!((r === 45 || r === 46) && r === e.input.charCodeAt(n + 1) && r === e.input.charCodeAt(n + 2) && (n += 3, r = e.input.charCodeAt(n), r === 0 || O(r)));
}
function un(e, n) {
  n === 1 ? e.result += " " : n > 1 && (e.result += S.repeat(`
`, n - 1));
}
function vl(e, n, r) {
  var i, l, t, o, u, s, c, f, a = e.kind, m = e.result, g;
  if (g = e.input.charCodeAt(e.position), O(g) || ne(g) || g === 35 || g === 38 || g === 42 || g === 33 || g === 124 || g === 62 || g === 39 || g === 34 || g === 37 || g === 64 || g === 96 || (g === 63 || g === 45) && (l = e.input.charCodeAt(e.position + 1), O(l) || r && ne(l)))
    return !1;
  for (e.kind = "scalar", e.result = "", t = o = e.position, u = !1; g !== 0; ) {
    if (g === 58) {
      if (l = e.input.charCodeAt(e.position + 1), O(l) || r && ne(l))
        break;
    } else if (g === 35) {
      if (i = e.input.charCodeAt(e.position - 1), O(i))
        break;
    } else {
      if (e.position === e.lineStart && Ke(e) || r && ne(g))
        break;
      if (B(g))
        if (s = e.line, c = e.lineStart, f = e.lineIndent, b(e, !1, -1), e.lineIndent >= n) {
          u = !0, g = e.input.charCodeAt(e.position);
          continue;
        } else {
          e.position = o, e.line = s, e.lineStart = c, e.lineIndent = f;
          break;
        }
    }
    u && (Y(e, t, o, !1), un(e, e.line - s), t = o = e.position, u = !1), z(g) || (o = e.position + 1), g = e.input.charCodeAt(++e.position);
  }
  return Y(e, t, o, !1), e.result ? !0 : (e.kind = a, e.result = m, !1);
}
function yl(e, n) {
  var r, i, l;
  if (r = e.input.charCodeAt(e.position), r !== 39)
    return !1;
  for (e.kind = "scalar", e.result = "", e.position++, i = l = e.position; (r = e.input.charCodeAt(e.position)) !== 0; )
    if (r === 39)
      if (Y(e, i, e.position, !0), r = e.input.charCodeAt(++e.position), r === 39)
        i = e.position, e.position++, l = e.position;
      else
        return !0;
    else
      B(r) ? (Y(e, i, l, !0), un(e, b(e, !1, n)), i = l = e.position) : e.position === e.lineStart && Ke(e) ? h(e, "unexpected end of the document within a single quoted scalar") : (e.position++, l = e.position);
  h(e, "unexpected end of the stream within a single quoted scalar");
}
function El(e, n) {
  var r, i, l, t, o, u;
  if (u = e.input.charCodeAt(e.position), u !== 34)
    return !1;
  for (e.kind = "scalar", e.result = "", e.position++, r = i = e.position; (u = e.input.charCodeAt(e.position)) !== 0; ) {
    if (u === 34)
      return Y(e, r, e.position, !0), e.position++, !0;
    if (u === 92) {
      if (Y(e, r, e.position, !0), u = e.input.charCodeAt(++e.position), B(u))
        b(e, !1, n);
      else if (u < 256 && wr[u])
        e.result += vr[u], e.position++;
      else if ((o = gl(u)) > 0) {
        for (l = o, t = 0; l > 0; l--)
          u = e.input.charCodeAt(++e.position), (o = ml(u)) >= 0 ? t = (t << 4) + o : h(e, "expected hexadecimal character");
        e.result += Cl(t), e.position++;
      } else
        h(e, "unknown escape sequence");
      r = i = e.position;
    } else
      B(u) ? (Y(e, r, i, !0), un(e, b(e, !1, n)), r = i = e.position) : e.position === e.lineStart && Ke(e) ? h(e, "unexpected end of the document within a double quoted scalar") : (e.position++, i = e.position);
  }
  h(e, "unexpected end of the stream within a double quoted scalar");
}
function Al(e, n) {
  var r = !0, i, l, t, o = e.tag, u, s = e.anchor, c, f, a, m, g, C = /* @__PURE__ */ Object.create(null), y, A, N, w;
  if (w = e.input.charCodeAt(e.position), w === 91)
    f = 93, g = !1, u = [];
  else if (w === 123)
    f = 125, g = !0, u = {};
  else
    return !1;
  for (e.anchor !== null && (e.anchorMap[e.anchor] = u), w = e.input.charCodeAt(++e.position); w !== 0; ) {
    if (b(e, !0, n), w = e.input.charCodeAt(e.position), w === f)
      return e.position++, e.tag = o, e.anchor = s, e.kind = g ? "mapping" : "sequence", e.result = u, !0;
    r ? w === 44 && h(e, "expected the node content, but found ','") : h(e, "missed comma between flow collection entries"), A = y = N = null, a = m = !1, w === 63 && (c = e.input.charCodeAt(e.position + 1), O(c) && (a = m = !0, e.position++, b(e, !0, n))), i = e.line, l = e.lineStart, t = e.position, se(e, n, Ie, !1, !0), A = e.tag, y = e.result, b(e, !0, n), w = e.input.charCodeAt(e.position), (m || e.line === i) && w === 58 && (a = !0, w = e.input.charCodeAt(++e.position), b(e, !0, n), se(e, n, Ie, !1, !0), N = e.result), g ? re(e, u, C, A, y, N, i, l, t) : a ? u.push(re(e, null, C, A, y, N, i, l, t)) : u.push(y), b(e, !0, n), w = e.input.charCodeAt(e.position), w === 44 ? (r = !0, w = e.input.charCodeAt(++e.position)) : r = !1;
  }
  h(e, "unexpected end of the stream within a flow collection");
}
function bl(e, n) {
  var r, i, l = We, t = !1, o = !1, u = n, s = 0, c = !1, f, a;
  if (a = e.input.charCodeAt(e.position), a === 124)
    i = !1;
  else if (a === 62)
    i = !0;
  else
    return !1;
  for (e.kind = "scalar", e.result = ""; a !== 0; )
    if (a = e.input.charCodeAt(++e.position), a === 43 || a === 45)
      We === l ? l = a === 43 ? gn : fl : h(e, "repeat of a chomping mode identifier");
    else if ((f = xl(a)) >= 0)
      f === 0 ? h(e, "bad explicit indentation width of a block scalar; it cannot be less than one") : o ? h(e, "repeat of an indentation width identifier") : (u = n + f - 1, o = !0);
    else
      break;
  if (z(a)) {
    do
      a = e.input.charCodeAt(++e.position);
    while (z(a));
    if (a === 35)
      do
        a = e.input.charCodeAt(++e.position);
      while (!B(a) && a !== 0);
  }
  for (; a !== 0; ) {
    for (on(e), e.lineIndent = 0, a = e.input.charCodeAt(e.position); (!o || e.lineIndent < u) && a === 32; )
      e.lineIndent++, a = e.input.charCodeAt(++e.position);
    if (!o && e.lineIndent > u && (u = e.lineIndent), B(a)) {
      s++;
      continue;
    }
    if (e.lineIndent < u) {
      l === gn ? e.result += S.repeat(`
`, t ? 1 + s : s) : l === We && t && (e.result += `
`);
      break;
    }
    for (i ? z(a) ? (c = !0, e.result += S.repeat(`
`, t ? 1 + s : s)) : c ? (c = !1, e.result += S.repeat(`
`, s + 1)) : s === 0 ? t && (e.result += " ") : e.result += S.repeat(`
`, s) : e.result += S.repeat(`
`, t ? 1 + s : s), t = !0, o = !0, s = 0, r = e.position; !B(a) && a !== 0; )
      a = e.input.charCodeAt(++e.position);
    Y(e, r, e.position, !1);
  }
  return !0;
}
function yn(e, n) {
  var r, i = e.tag, l = e.anchor, t = [], o, u = !1, s;
  if (e.firstTabInLine !== -1)
    return !1;
  for (e.anchor !== null && (e.anchorMap[e.anchor] = t), s = e.input.charCodeAt(e.position); s !== 0 && (e.firstTabInLine !== -1 && (e.position = e.firstTabInLine, h(e, "tab characters must not be used in indentation")), !(s !== 45 || (o = e.input.charCodeAt(e.position + 1), !O(o)))); ) {
    if (u = !0, e.position++, b(e, !0, -1) && e.lineIndent <= n) {
      t.push(null), s = e.input.charCodeAt(e.position);
      continue;
    }
    if (r = e.line, se(e, n, gr, !1, !0), t.push(e.result), b(e, !0, -1), s = e.input.charCodeAt(e.position), (e.line === r || e.lineIndent > n) && s !== 0)
      h(e, "bad indentation of a sequence entry");
    else if (e.lineIndent < n)
      break;
  }
  return u ? (e.tag = i, e.anchor = l, e.kind = "sequence", e.result = t, !0) : !1;
}
function Sl(e, n, r) {
  var i, l, t, o, u, s, c = e.tag, f = e.anchor, a = {}, m = /* @__PURE__ */ Object.create(null), g = null, C = null, y = null, A = !1, N = !1, w;
  if (e.firstTabInLine !== -1)
    return !1;
  for (e.anchor !== null && (e.anchorMap[e.anchor] = a), w = e.input.charCodeAt(e.position); w !== 0; ) {
    if (!A && e.firstTabInLine !== -1 && (e.position = e.firstTabInLine, h(e, "tab characters must not be used in indentation")), i = e.input.charCodeAt(e.position + 1), t = e.line, (w === 63 || w === 58) && O(i))
      w === 63 ? (A && (re(e, a, m, g, C, null, o, u, s), g = C = y = null), N = !0, A = !0, l = !0) : A ? (A = !1, l = !0) : h(e, "incomplete explicit mapping pair; a key node is missed; or followed by a non-tabulated empty line"), e.position += 1, w = i;
    else {
      if (o = e.line, u = e.lineStart, s = e.position, !se(e, r, mr, !1, !0))
        break;
      if (e.line === t) {
        for (w = e.input.charCodeAt(e.position); z(w); )
          w = e.input.charCodeAt(++e.position);
        if (w === 58)
          w = e.input.charCodeAt(++e.position), O(w) || h(e, "a whitespace character is expected after the key-value separator within a block mapping"), A && (re(e, a, m, g, C, null, o, u, s), g = C = y = null), N = !0, A = !1, l = !1, g = e.tag, C = e.result;
        else if (N)
          h(e, "can not read an implicit mapping pair; a colon is missed");
        else
          return e.tag = c, e.anchor = f, !0;
      } else if (N)
        h(e, "can not read a block mapping entry; a multiline key may not be an implicit key");
      else
        return e.tag = c, e.anchor = f, !0;
    }
    if ((e.line === t || e.lineIndent > n) && (A && (o = e.line, u = e.lineStart, s = e.position), se(e, n, Fe, !0, l) && (A ? C = e.result : y = e.result), A || (re(e, a, m, g, C, y, o, u, s), g = C = y = null), b(e, !0, -1), w = e.input.charCodeAt(e.position)), (e.line === t || e.lineIndent > n) && w !== 0)
      h(e, "bad indentation of a mapping entry");
    else if (e.lineIndent < n)
      break;
  }
  return A && re(e, a, m, g, C, null, o, u, s), N && (e.tag = c, e.anchor = f, e.kind = "mapping", e.result = a), N;
}
function Tl(e) {
  var n, r = !1, i = !1, l, t, o;
  if (o = e.input.charCodeAt(e.position), o !== 33)
    return !1;
  if (e.tag !== null && h(e, "duplication of a tag property"), o = e.input.charCodeAt(++e.position), o === 60 ? (r = !0, o = e.input.charCodeAt(++e.position)) : o === 33 ? (i = !0, l = "!!", o = e.input.charCodeAt(++e.position)) : l = "!", n = e.position, r) {
    do
      o = e.input.charCodeAt(++e.position);
    while (o !== 0 && o !== 62);
    e.position < e.length ? (t = e.input.slice(n, e.position), o = e.input.charCodeAt(++e.position)) : h(e, "unexpected end of the stream within a verbatim tag");
  } else {
    for (; o !== 0 && !O(o); )
      o === 33 && (i ? h(e, "tag suffix cannot contain exclamation marks") : (l = e.input.slice(n - 1, e.position + 1), xr.test(l) || h(e, "named tag handle cannot contain such characters"), i = !0, n = e.position + 1)), o = e.input.charCodeAt(++e.position);
    t = e.input.slice(n, e.position), pl.test(t) && h(e, "tag suffix cannot contain flow indicator characters");
  }
  t && !Cr.test(t) && h(e, "tag name cannot contain such characters: " + t);
  try {
    t = decodeURIComponent(t);
  } catch {
    h(e, "tag name is malformed: " + t);
  }
  return r ? e.tag = t : K.call(e.tagMap, l) ? e.tag = e.tagMap[l] + t : l === "!" ? e.tag = "!" + t : l === "!!" ? e.tag = "tag:yaml.org,2002:" + t : h(e, 'undeclared tag handle "' + l + '"'), !0;
}
function _l(e) {
  var n, r;
  if (r = e.input.charCodeAt(e.position), r !== 38)
    return !1;
  for (e.anchor !== null && h(e, "duplication of an anchor property"), r = e.input.charCodeAt(++e.position), n = e.position; r !== 0 && !O(r) && !ne(r); )
    r = e.input.charCodeAt(++e.position);
  return e.position === n && h(e, "name of an anchor node must contain at least one character"), e.anchor = e.input.slice(n, e.position), !0;
}
function Ll(e) {
  var n, r, i;
  if (i = e.input.charCodeAt(e.position), i !== 42)
    return !1;
  for (i = e.input.charCodeAt(++e.position), n = e.position; i !== 0 && !O(i) && !ne(i); )
    i = e.input.charCodeAt(++e.position);
  return e.position === n && h(e, "name of an alias node must contain at least one character"), r = e.input.slice(n, e.position), K.call(e.anchorMap, r) || h(e, 'unidentified alias "' + r + '"'), e.result = e.anchorMap[r], b(e, !0, -1), !0;
}
function se(e, n, r, i, l) {
  var t, o, u, s = 1, c = !1, f = !1, a, m, g, C, y, A;
  if (e.listener !== null && e.listener("open", e), e.tag = null, e.anchor = null, e.kind = null, e.result = null, t = o = u = Fe === r || gr === r, i && b(e, !0, -1) && (c = !0, e.lineIndent > n ? s = 1 : e.lineIndent === n ? s = 0 : e.lineIndent < n && (s = -1)), s === 1)
    for (; Tl(e) || _l(e); )
      b(e, !0, -1) ? (c = !0, u = t, e.lineIndent > n ? s = 1 : e.lineIndent === n ? s = 0 : e.lineIndent < n && (s = -1)) : u = !1;
  if (u && (u = c || l), (s === 1 || Fe === r) && (Ie === r || mr === r ? y = n : y = n + 1, A = e.position - e.lineStart, s === 1 ? u && (yn(e, A) || Sl(e, A, y)) || Al(e, y) ? f = !0 : (o && bl(e, y) || yl(e, y) || El(e, y) ? f = !0 : Ll(e) ? (f = !0, (e.tag !== null || e.anchor !== null) && h(e, "alias node should not have any properties")) : vl(e, y, Ie === r) && (f = !0, e.tag === null && (e.tag = "?")), e.anchor !== null && (e.anchorMap[e.anchor] = e.result)) : s === 0 && (f = u && yn(e, A))), e.tag === null)
    e.anchor !== null && (e.anchorMap[e.anchor] = e.result);
  else if (e.tag === "?") {
    for (e.result !== null && e.kind !== "scalar" && h(e, 'unacceptable node kind for !<?> tag; it should be "scalar", not "' + e.kind + '"'), a = 0, m = e.implicitTypes.length; a < m; a += 1)
      if (C = e.implicitTypes[a], C.resolve(e.result)) {
        e.result = C.construct(e.result), e.tag = C.tag, e.anchor !== null && (e.anchorMap[e.anchor] = e.result);
        break;
      }
  } else if (e.tag !== "!") {
    if (K.call(e.typeMap[e.kind || "fallback"], e.tag))
      C = e.typeMap[e.kind || "fallback"][e.tag];
    else
      for (C = null, g = e.typeMap.multi[e.kind || "fallback"], a = 0, m = g.length; a < m; a += 1)
        if (e.tag.slice(0, g[a].tag.length) === g[a].tag) {
          C = g[a];
          break;
        }
    C || h(e, "unknown tag !<" + e.tag + ">"), e.result !== null && C.kind !== e.kind && h(e, "unacceptable node kind for !<" + e.tag + '> tag; it should be "' + C.kind + '", not "' + e.kind + '"'), C.resolve(e.result, e.tag) ? (e.result = C.construct(e.result, e.tag), e.anchor !== null && (e.anchorMap[e.anchor] = e.result)) : h(e, "cannot resolve a node with !<" + e.tag + "> explicit tag");
  }
  return e.listener !== null && e.listener("close", e), e.tag !== null || e.anchor !== null || f;
}
function kl(e) {
  var n = e.position, r, i, l, t = !1, o;
  for (e.version = null, e.checkLineBreaks = e.legacy, e.tagMap = /* @__PURE__ */ Object.create(null), e.anchorMap = /* @__PURE__ */ Object.create(null); (o = e.input.charCodeAt(e.position)) !== 0 && (b(e, !0, -1), o = e.input.charCodeAt(e.position), !(e.lineIndent > 0 || o !== 37)); ) {
    for (t = !0, o = e.input.charCodeAt(++e.position), r = e.position; o !== 0 && !O(o); )
      o = e.input.charCodeAt(++e.position);
    for (i = e.input.slice(r, e.position), l = [], i.length < 1 && h(e, "directive name must not be less than one character in length"); o !== 0; ) {
      for (; z(o); )
        o = e.input.charCodeAt(++e.position);
      if (o === 35) {
        do
          o = e.input.charCodeAt(++e.position);
        while (o !== 0 && !B(o));
        break;
      }
      if (B(o))
        break;
      for (r = e.position; o !== 0 && !O(o); )
        o = e.input.charCodeAt(++e.position);
      l.push(e.input.slice(r, e.position));
    }
    o !== 0 && on(e), K.call(wn, i) ? wn[i](e, i, l) : Oe(e, 'unknown document directive "' + i + '"');
  }
  if (b(e, !0, -1), e.lineIndent === 0 && e.input.charCodeAt(e.position) === 45 && e.input.charCodeAt(e.position + 1) === 45 && e.input.charCodeAt(e.position + 2) === 45 ? (e.position += 3, b(e, !0, -1)) : t && h(e, "directives end mark is expected"), se(e, e.lineIndent - 1, Fe, !1, !0), b(e, !0, -1), e.checkLineBreaks && hl.test(e.input.slice(n, e.position)) && Oe(e, "non-ASCII line breaks are interpreted as content"), e.documents.push(e.result), e.position === e.lineStart && Ke(e)) {
    e.input.charCodeAt(e.position) === 46 && (e.position += 3, b(e, !0, -1));
    return;
  }
  if (e.position < e.length - 1)
    h(e, "end of the stream or a document separator is expected");
  else
    return;
}
function Er(e, n) {
  e = String(e), n = n || {}, e.length !== 0 && (e.charCodeAt(e.length - 1) !== 10 && e.charCodeAt(e.length - 1) !== 13 && (e += `
`), e.charCodeAt(0) === 65279 && (e = e.slice(1)));
  var r = new wl(e, n), i = e.indexOf("\0");
  for (i !== -1 && (r.position = i, h(r, "null byte is not allowed in input")), r.input += "\0"; r.input.charCodeAt(r.position) === 32; )
    r.lineIndent += 1, r.position += 1;
  for (; r.position < r.length - 1; )
    kl(r);
  return r.documents;
}
function Il(e, n, r) {
  n !== null && typeof n == "object" && typeof r > "u" && (r = n, n = null);
  var i = Er(e, r);
  if (typeof n != "function")
    return i;
  for (var l = 0, t = i.length; l < t; l += 1)
    n(i[l]);
}
function Fl(e, n) {
  var r = Er(e, n);
  if (r.length !== 0) {
    if (r.length === 1)
      return r[0];
    throw new F("expected a single document in the stream, but found more");
  }
}
var Ol = Il, Nl = Fl, Ar = {
  loadAll: Ol,
  load: Nl
}, br = Object.prototype.toString, Sr = Object.prototype.hasOwnProperty, sn = 65279, $l = 9, he = 10, Rl = 13, Dl = 32, Ml = 33, Bl = 34, ze = 35, Hl = 37, jl = 38, Pl = 39, Ul = 42, Tr = 44, Yl = 45, Ne = 58, Kl = 61, Vl = 62, ql = 63, Gl = 64, _r = 91, Lr = 93, Wl = 96, kr = 123, Ql = 124, Ir = 125, L = {};
L[0] = "\\0";
L[7] = "\\a";
L[8] = "\\b";
L[9] = "\\t";
L[10] = "\\n";
L[11] = "\\v";
L[12] = "\\f";
L[13] = "\\r";
L[27] = "\\e";
L[34] = '\\"';
L[92] = "\\\\";
L[133] = "\\N";
L[160] = "\\_";
L[8232] = "\\L";
L[8233] = "\\P";
var zl = [
  "y",
  "Y",
  "yes",
  "Yes",
  "YES",
  "on",
  "On",
  "ON",
  "n",
  "N",
  "no",
  "No",
  "NO",
  "off",
  "Off",
  "OFF"
], Xl = /^[-+]?[0-9_]+(?::[0-9_]+)+(?:\.[0-9_]*)?$/;
function Zl(e, n) {
  var r, i, l, t, o, u, s;
  if (n === null)
    return {};
  for (r = {}, i = Object.keys(n), l = 0, t = i.length; l < t; l += 1)
    o = i[l], u = String(n[o]), o.slice(0, 2) === "!!" && (o = "tag:yaml.org,2002:" + o.slice(2)), s = e.compiledTypeMap.fallback[o], s && Sr.call(s.styleAliases, u) && (u = s.styleAliases[u]), r[o] = u;
  return r;
}
function Jl(e) {
  var n, r, i;
  if (n = e.toString(16).toUpperCase(), e <= 255)
    r = "x", i = 2;
  else if (e <= 65535)
    r = "u", i = 4;
  else if (e <= 4294967295)
    r = "U", i = 8;
  else
    throw new F("code point within a string may not be greater than 0xFFFFFFFF");
  return "\\" + r + S.repeat("0", i - n.length) + n;
}
var et = 1, pe = 2;
function nt(e) {
  this.schema = e.schema || tn, this.indent = Math.max(1, e.indent || 2), this.noArrayIndent = e.noArrayIndent || !1, this.skipInvalid = e.skipInvalid || !1, this.flowLevel = S.isNothing(e.flowLevel) ? -1 : e.flowLevel, this.styleMap = Zl(this.schema, e.styles || null), this.sortKeys = e.sortKeys || !1, this.lineWidth = e.lineWidth || 80, this.noRefs = e.noRefs || !1, this.noCompatMode = e.noCompatMode || !1, this.condenseFlow = e.condenseFlow || !1, this.quotingType = e.quotingType === '"' ? pe : et, this.forceQuotes = e.forceQuotes || !1, this.replacer = typeof e.replacer == "function" ? e.replacer : null, this.implicitTypes = this.schema.compiledImplicit, this.explicitTypes = this.schema.compiledExplicit, this.tag = null, this.result = "", this.duplicates = [], this.usedDuplicates = null;
}
function En(e, n) {
  for (var r = S.repeat(" ", n), i = 0, l = -1, t = "", o, u = e.length; i < u; )
    l = e.indexOf(`
`, i), l === -1 ? (o = e.slice(i), i = u) : (o = e.slice(i, l + 1), i = l + 1), o.length && o !== `
` && (t += r), t += o;
  return t;
}
function Xe(e, n) {
  return `
` + S.repeat(" ", e.indent * n);
}
function rt(e, n) {
  var r, i, l;
  for (r = 0, i = e.implicitTypes.length; r < i; r += 1)
    if (l = e.implicitTypes[r], l.resolve(n))
      return !0;
  return !1;
}
function $e(e) {
  return e === Dl || e === $l;
}
function me(e) {
  return 32 <= e && e <= 126 || 161 <= e && e <= 55295 && e !== 8232 && e !== 8233 || 57344 <= e && e <= 65533 && e !== sn || 65536 <= e && e <= 1114111;
}
function An(e) {
  return me(e) && e !== sn && e !== Rl && e !== he;
}
function bn(e, n, r) {
  var i = An(e), l = i && !$e(e);
  return (
    // ns-plain-safe
    (r ? (
      // c = flow-in
      i
    ) : i && e !== Tr && e !== _r && e !== Lr && e !== kr && e !== Ir) && e !== ze && !(n === Ne && !l) || An(n) && !$e(n) && e === ze || n === Ne && l
  );
}
function it(e) {
  return me(e) && e !== sn && !$e(e) && e !== Yl && e !== ql && e !== Ne && e !== Tr && e !== _r && e !== Lr && e !== kr && e !== Ir && e !== ze && e !== jl && e !== Ul && e !== Ml && e !== Ql && e !== Kl && e !== Vl && e !== Pl && e !== Bl && e !== Hl && e !== Gl && e !== Wl;
}
function lt(e) {
  return !$e(e) && e !== Ne;
}
function ce(e, n) {
  var r = e.charCodeAt(n), i;
  return r >= 55296 && r <= 56319 && n + 1 < e.length && (i = e.charCodeAt(n + 1), i >= 56320 && i <= 57343) ? (r - 55296) * 1024 + i - 56320 + 65536 : r;
}
function Fr(e) {
  var n = /^\n* /;
  return n.test(e);
}
var Or = 1, Ze = 2, Nr = 3, $r = 4, J = 5;
function tt(e, n, r, i, l, t, o, u) {
  var s, c = 0, f = null, a = !1, m = !1, g = i !== -1, C = -1, y = it(ce(e, 0)) && lt(ce(e, e.length - 1));
  if (n || o)
    for (s = 0; s < e.length; c >= 65536 ? s += 2 : s++) {
      if (c = ce(e, s), !me(c))
        return J;
      y = y && bn(c, f, u), f = c;
    }
  else {
    for (s = 0; s < e.length; c >= 65536 ? s += 2 : s++) {
      if (c = ce(e, s), c === he)
        a = !0, g && (m = m || // Foldable line = too long, and not more-indented.
        s - C - 1 > i && e[C + 1] !== " ", C = s);
      else if (!me(c))
        return J;
      y = y && bn(c, f, u), f = c;
    }
    m = m || g && s - C - 1 > i && e[C + 1] !== " ";
  }
  return !a && !m ? y && !o && !l(e) ? Or : t === pe ? J : Ze : r > 9 && Fr(e) ? J : o ? t === pe ? J : Ze : m ? $r : Nr;
}
function ot(e, n, r, i, l) {
  e.dump = function() {
    if (n.length === 0)
      return e.quotingType === pe ? '""' : "''";
    if (!e.noCompatMode && (zl.indexOf(n) !== -1 || Xl.test(n)))
      return e.quotingType === pe ? '"' + n + '"' : "'" + n + "'";
    var t = e.indent * Math.max(1, r), o = e.lineWidth === -1 ? -1 : Math.max(Math.min(e.lineWidth, 40), e.lineWidth - t), u = i || e.flowLevel > -1 && r >= e.flowLevel;
    function s(c) {
      return rt(e, c);
    }
    switch (tt(
      n,
      u,
      e.indent,
      o,
      s,
      e.quotingType,
      e.forceQuotes && !i,
      l
    )) {
      case Or:
        return n;
      case Ze:
        return "'" + n.replace(/'/g, "''") + "'";
      case Nr:
        return "|" + Sn(n, e.indent) + Tn(En(n, t));
      case $r:
        return ">" + Sn(n, e.indent) + Tn(En(ut(n, o), t));
      case J:
        return '"' + st(n) + '"';
      default:
        throw new F("impossible error: invalid scalar style");
    }
  }();
}
function Sn(e, n) {
  var r = Fr(e) ? String(n) : "", i = e[e.length - 1] === `
`, l = i && (e[e.length - 2] === `
` || e === `
`), t = l ? "+" : i ? "" : "-";
  return r + t + `
`;
}
function Tn(e) {
  return e[e.length - 1] === `
` ? e.slice(0, -1) : e;
}
function ut(e, n) {
  for (var r = /(\n+)([^\n]*)/g, i = function() {
    var c = e.indexOf(`
`);
    return c = c !== -1 ? c : e.length, r.lastIndex = c, _n(e.slice(0, c), n);
  }(), l = e[0] === `
` || e[0] === " ", t, o; o = r.exec(e); ) {
    var u = o[1], s = o[2];
    t = s[0] === " ", i += u + (!l && !t && s !== "" ? `
` : "") + _n(s, n), l = t;
  }
  return i;
}
function _n(e, n) {
  if (e === "" || e[0] === " ")
    return e;
  for (var r = / [^ ]/g, i, l = 0, t, o = 0, u = 0, s = ""; i = r.exec(e); )
    u = i.index, u - l > n && (t = o > l ? o : u, s += `
` + e.slice(l, t), l = t + 1), o = u;
  return s += `
`, e.length - l > n && o > l ? s += e.slice(l, o) + `
` + e.slice(o + 1) : s += e.slice(l), s.slice(1);
}
function st(e) {
  for (var n = "", r = 0, i, l = 0; l < e.length; r >= 65536 ? l += 2 : l++)
    r = ce(e, l), i = L[r], !i && me(r) ? (n += e[l], r >= 65536 && (n += e[l + 1])) : n += i || Jl(r);
  return n;
}
function ct(e, n, r) {
  var i = "", l = e.tag, t, o, u;
  for (t = 0, o = r.length; t < o; t += 1)
    u = r[t], e.replacer && (u = e.replacer.call(r, String(t), u)), (H(e, n, u, !1, !1) || typeof u > "u" && H(e, n, null, !1, !1)) && (i !== "" && (i += "," + (e.condenseFlow ? "" : " ")), i += e.dump);
  e.tag = l, e.dump = "[" + i + "]";
}
function Ln(e, n, r, i) {
  var l = "", t = e.tag, o, u, s;
  for (o = 0, u = r.length; o < u; o += 1)
    s = r[o], e.replacer && (s = e.replacer.call(r, String(o), s)), (H(e, n + 1, s, !0, !0, !1, !0) || typeof s > "u" && H(e, n + 1, null, !0, !0, !1, !0)) && ((!i || l !== "") && (l += Xe(e, n)), e.dump && he === e.dump.charCodeAt(0) ? l += "-" : l += "- ", l += e.dump);
  e.tag = t, e.dump = l || "[]";
}
function at(e, n, r) {
  var i = "", l = e.tag, t = Object.keys(r), o, u, s, c, f;
  for (o = 0, u = t.length; o < u; o += 1)
    f = "", i !== "" && (f += ", "), e.condenseFlow && (f += '"'), s = t[o], c = r[s], e.replacer && (c = e.replacer.call(r, s, c)), H(e, n, s, !1, !1) && (e.dump.length > 1024 && (f += "? "), f += e.dump + (e.condenseFlow ? '"' : "") + ":" + (e.condenseFlow ? "" : " "), H(e, n, c, !1, !1) && (f += e.dump, i += f));
  e.tag = l, e.dump = "{" + i + "}";
}
function ft(e, n, r, i) {
  var l = "", t = e.tag, o = Object.keys(r), u, s, c, f, a, m;
  if (e.sortKeys === !0)
    o.sort();
  else if (typeof e.sortKeys == "function")
    o.sort(e.sortKeys);
  else if (e.sortKeys)
    throw new F("sortKeys must be a boolean or a function");
  for (u = 0, s = o.length; u < s; u += 1)
    m = "", (!i || l !== "") && (m += Xe(e, n)), c = o[u], f = r[c], e.replacer && (f = e.replacer.call(r, c, f)), H(e, n + 1, c, !0, !0, !0) && (a = e.tag !== null && e.tag !== "?" || e.dump && e.dump.length > 1024, a && (e.dump && he === e.dump.charCodeAt(0) ? m += "?" : m += "? "), m += e.dump, a && (m += Xe(e, n)), H(e, n + 1, f, !0, a) && (e.dump && he === e.dump.charCodeAt(0) ? m += ":" : m += ": ", m += e.dump, l += m));
  e.tag = t, e.dump = l || "{}";
}
function kn(e, n, r) {
  var i, l, t, o, u, s;
  for (l = r ? e.explicitTypes : e.implicitTypes, t = 0, o = l.length; t < o; t += 1)
    if (u = l[t], (u.instanceOf || u.predicate) && (!u.instanceOf || typeof n == "object" && n instanceof u.instanceOf) && (!u.predicate || u.predicate(n))) {
      if (r ? u.multi && u.representName ? e.tag = u.representName(n) : e.tag = u.tag : e.tag = "?", u.represent) {
        if (s = e.styleMap[u.tag] || u.defaultStyle, br.call(u.represent) === "[object Function]")
          i = u.represent(n, s);
        else if (Sr.call(u.represent, s))
          i = u.represent[s](n, s);
        else
          throw new F("!<" + u.tag + '> tag resolver accepts not "' + s + '" style');
        e.dump = i;
      }
      return !0;
    }
  return !1;
}
function H(e, n, r, i, l, t, o) {
  e.tag = null, e.dump = r, kn(e, r, !1) || kn(e, r, !0);
  var u = br.call(e.dump), s = i, c;
  i && (i = e.flowLevel < 0 || e.flowLevel > n);
  var f = u === "[object Object]" || u === "[object Array]", a, m;
  if (f && (a = e.duplicates.indexOf(r), m = a !== -1), (e.tag !== null && e.tag !== "?" || m || e.indent !== 2 && n > 0) && (l = !1), m && e.usedDuplicates[a])
    e.dump = "*ref_" + a;
  else {
    if (f && m && !e.usedDuplicates[a] && (e.usedDuplicates[a] = !0), u === "[object Object]")
      i && Object.keys(e.dump).length !== 0 ? (ft(e, n, e.dump, l), m && (e.dump = "&ref_" + a + e.dump)) : (at(e, n, e.dump), m && (e.dump = "&ref_" + a + " " + e.dump));
    else if (u === "[object Array]")
      i && e.dump.length !== 0 ? (e.noArrayIndent && !o && n > 0 ? Ln(e, n - 1, e.dump, l) : Ln(e, n, e.dump, l), m && (e.dump = "&ref_" + a + e.dump)) : (ct(e, n, e.dump), m && (e.dump = "&ref_" + a + " " + e.dump));
    else if (u === "[object String]")
      e.tag !== "?" && ot(e, e.dump, n, t, s);
    else {
      if (u === "[object Undefined]")
        return !1;
      if (e.skipInvalid)
        return !1;
      throw new F("unacceptable kind of an object to dump " + u);
    }
    e.tag !== null && e.tag !== "?" && (c = encodeURI(
      e.tag[0] === "!" ? e.tag.slice(1) : e.tag
    ).replace(/!/g, "%21"), e.tag[0] === "!" ? c = "!" + c : c.slice(0, 18) === "tag:yaml.org,2002:" ? c = "!!" + c.slice(18) : c = "!<" + c + ">", e.dump = c + " " + e.dump);
  }
  return !0;
}
function dt(e, n) {
  var r = [], i = [], l, t;
  for (Je(e, r, i), l = 0, t = i.length; l < t; l += 1)
    n.duplicates.push(r[i[l]]);
  n.usedDuplicates = new Array(t);
}
function Je(e, n, r) {
  var i, l, t;
  if (e !== null && typeof e == "object")
    if (l = n.indexOf(e), l !== -1)
      r.indexOf(l) === -1 && r.push(l);
    else if (n.push(e), Array.isArray(e))
      for (l = 0, t = e.length; l < t; l += 1)
        Je(e[l], n, r);
    else
      for (i = Object.keys(e), l = 0, t = i.length; l < t; l += 1)
        Je(e[i[l]], n, r);
}
function ht(e, n) {
  n = n || {};
  var r = new nt(n);
  r.noRefs || dt(e, r);
  var i = e;
  return r.replacer && (i = r.replacer.call({ "": i }, "", i)), H(r, 0, i, !0, !0) ? r.dump + `
` : "";
}
var pt = ht, mt = {
  dump: pt
};
function cn(e, n) {
  return function() {
    throw new Error("Function yaml." + e + " is removed in js-yaml 4. Use yaml." + n + " instead, which is now safe by default.");
  };
}
var gt = T, xt = zn, Ct = er, wt = tr, vt = or, yt = tn, Et = Ar.load, At = Ar.loadAll, bt = mt.dump, St = F, Tt = {
  binary: fr,
  float: lr,
  map: Jn,
  null: nr,
  pairs: hr,
  set: pr,
  timestamp: cr,
  bool: rr,
  int: ir,
  merge: ar,
  omap: dr,
  seq: Zn,
  str: Xn
}, _t = cn("safeLoad", "load"), Lt = cn("safeLoadAll", "loadAll"), kt = cn("safeDump", "dump"), It = {
  Type: gt,
  Schema: xt,
  FAILSAFE_SCHEMA: Ct,
  JSON_SCHEMA: wt,
  CORE_SCHEMA: vt,
  DEFAULT_SCHEMA: yt,
  load: Et,
  loadAll: At,
  dump: bt,
  YAMLException: St,
  types: Tt,
  safeLoad: _t,
  safeLoadAll: Lt,
  safeDump: kt
};
const Ft = "LabelText.ClueText(LengthText)", Rr = /^\s*(.*?)\.(.*)\((.*)\)\s*$/, In = /^([^bce-z]*?)(\d+[ad]?)\s*(.*)/, Ot = /^\s*(.*?)\s*$/, Fn = /^([^a-z()\d]*?)(\d+)[\s.]*(.*)/, Nt = /(.*?)(\*\*.+?\*\*)(.*)$/, $t = /(.*?)(\*\*\*.+?\*\*\*)(.*)$/, Rt = /(.*?)(\*[^*]+?\*)(.*)$/, Dt = /(.*?)(__.+?__)(.*)$/, Mt = /(.*?)(___.+?___)(.*)$/, Bt = /(.*?)(_[^_]+?_)(.*)$/, Ht = [
  {
    tag: "***",
    regex: $t,
    html: { open: '<span class="cw-bold cw-italic">', close: "</span>" }
  },
  {
    tag: "___",
    regex: Mt,
    html: { open: '<span class="cw-bold cw-italic">', close: "</span>" }
  },
  {
    tag: "**",
    regex: Nt,
    html: { open: '<span class="cw-bold">', close: "</span>" }
  },
  {
    tag: "__",
    regex: Dt,
    html: { open: '<span class="cw-bold">', close: "</span>" }
  },
  {
    tag: "*",
    regex: Rt,
    html: { open: '<span class="cw-italic">', close: "</span>" }
  },
  {
    tag: "_",
    regex: Bt,
    html: { open: '<span class="cw-italic">', close: "</span>" }
  }
];
function jt(e) {
  let n = e;
  return Ht.forEach((r) => {
    let i, l, t = n;
    if (r.regex.test(t)) {
      let o = r.regex.exec(t);
      for (n = ""; (o == null ? void 0 : o.length) === 4; )
        [, i, l, t] = o, l = l.replace(r.tag, r.html.open), l = l.replace(r.tag, r.html.close), n += i + l, o = r.regex.exec(t);
      n += t;
    }
  }), n;
}
function Pt(e) {
  const n = { x: 1, y: 1, clue: "1. Clue (1)" }, r = { answer: "", solution: "", revealed: "" }, i = Object.keys(n), l = Object.keys(r), t = Object.keys(e);
  for (const u of i)
    if (!t.includes(u))
      throw new Error(`'cdClue.${u}' is missing`);
  for (const u of i)
    if (typeof n[u] != typeof e[u])
      throw new Error(
        `'cdClue.${u} (${e[u]})' must be a ${typeof n[u]}`
      );
  for (const u of l)
    if (t.includes(u) && typeof r[u] != typeof e[u])
      throw new Error(
        `'cdClue.${u} (${e[u]})' must be a ${typeof r[u]}`
      );
  const o = new Set(t);
  for (const u of i)
    o.delete(u);
  for (const u of l)
    o.delete(u);
  if (o.size > 0)
    throw new Error(
      `'cdClue' has unexpected properties <${[...o].join(",")}>`
    );
  if (!Rr.test(e.clue))
    throw new Error(
      `Clue '${e.clue}' does not match the required pattern '${Ft}'`
    );
}
function Ut(e, n) {
  if (e === void 0 || n === void 0)
    throw new Error("'cdClue' and 'isAcrossClue' are required");
  if (e === null)
    throw new Error("'cdClue' can't be null");
  if (n === null)
    throw new Error("'isAcrossClue' can't be null");
  if (typeof n != "boolean")
    throw new Error("'isAcrossClue' must be a boolean (true,false)");
}
function Yt(e, n) {
  let r = e.toLowerCase(), i = [];
  for (; In.test(r); ) {
    const [, , l, t] = In.exec(r);
    i.push(l), r = t;
  }
  if (r)
    throw new Error(
      `'${n.clue}' Error in <LabelText> near <${r}>`
    );
  return i;
}
function Kt(e) {
  function n(l) {
    return l.endsWith("a") ? "across" : l.endsWith("d") ? "down" : null;
  }
  let r = e.slice(1), i = [];
  return r.length > 0 && (i = r.map((l) => ({
    headNumber: parseInt(l, 10),
    direction: n(l)
  }))), i;
}
function Vt(e, n) {
  let r = [], i = e;
  for (; Fn.test(i); ) {
    const [, , l, t] = Fn.exec(i);
    r.push(parseInt(l, 10)), i = t;
  }
  if (i)
    throw new Error(
      `'${n.clue}' Error in <LengthText> near <${i}>`
    );
  return r;
}
const qt = (e, n) => {
  const r = (l) => l ? "a" : "d";
  return /[ad]$/.test(e) ? e : e + r(n);
};
function Gt(e, n) {
  Ut(e, n), Pt(e);
  const r = [], i = e.x - 1, l = e.y - 1, t = n, o = e.solution ? (
    // Strip out everything from solution except alphabetical characters
    // DO NOT substitute spaces
    e.solution.toUpperCase().replaceAll(/[^A-Z]/g, "")
  ) : void 0, u = e.revealed ? (
    // string of upper-cased revealed characters
    e.revealed.toUpperCase()
  ) : void 0, [, s, c, f] = Rr.exec(e.clue), a = Yt(s, e), m = Kt(a), [g] = a, C = parseInt(g, 10), y = C.toString(), A = qt(g, t), [, N] = Ot.exec(c), w = jt(N), an = `(${f})`, fn = Vt(f, e), X = fn.reduce((Ur, Yr) => Ur + Yr, 0), Pr = e.answer ? e.answer.toUpperCase().replaceAll(/[^ A-Z]/g, " ").padEnd(X) : (
    // pad out null or undefined answer with spaces
    "".padEnd(X)
  );
  if (o && o.length !== X)
    throw new Error(
      `Length of clue solution '${o}' does not match the lengthText '${an}'`
    );
  if (u && u.length !== X)
    throw new Error(
      `Length of clue revealed characters '${u}' does not match the lengthText: ${X}`
    );
  return {
    answer: Pr,
    cells: r,
    clueId: A,
    clueText: w,
    headNumber: C,
    isAcross: t,
    labelText: y,
    lengthText: an,
    revealed: u,
    segmentLength: X,
    solution: o,
    tailDescriptors: m,
    wordLengths: fn,
    x: i,
    y: l,
    toString: () => `${A}`
  };
}
function Wt(e) {
  if (x("newCrosswordModel"), !Dr(e))
    return x(
      "newCrosswordModel: The model must be initialised with a valid crossword definition.",
      "error"
    ), null;
  let n = Xt(e);
  n.cells = Qt(n);
  const r = /across/i;
  return ["acrossClues", "downClues"].forEach((i) => {
    e[i].forEach(
      no(n, r.test(i))
    );
  }), [...n.acrossClues, ...n.downClues].forEach(
    io(n)
  ), n.lightCells = n.cells.flat().filter((i) => i.light), ["acrossClues", "downClues"].forEach((i) => {
    n[i].headSegments = n[i].filter(
      (l) => l === l.headSegment
    );
  }), n;
}
function Qt(e) {
  const { width: n } = e, { height: r } = e, i = new Array(n);
  for (let l = 0; l < n; l += 1) {
    i[l] = new Array(r);
    for (let t = 0; t < r; t += 1)
      i[l][t] = {
        model: e,
        x: l,
        y: t,
        toString: () => `${l},${t}`
      };
  }
  return i;
}
function zt(e, n) {
  if (e >= 0) {
    let r = e, i = 0;
    for (; i < n.length; ) {
      const l = n[i];
      if (r < l)
        return (
          // is a word terminator
          r === l - 1 && //  is not last word
          i !== n.length - 1
        );
      r -= l, i += 1;
    }
  }
  return !1;
}
function Xt(e) {
  let n = {
    width: e.width,
    height: e.height,
    acrossClues: [],
    downClues: [],
    cells: []
  };
  if (n.width === void 0 || n.width === null || n.width < 0 || n.height === void 0 || n.height === null || n.height < 0)
    throw new Error("The crossword bounds are invalid.");
  return n;
}
function Dr(e) {
  var t, o;
  const n = /^1\.0$/;
  function r(u) {
    return x(`validateCrosswordDefinition: ${u}`, "error"), !1;
  }
  function i(u) {
    return u.toString().trim().toLowerCase();
  }
  const l = e;
  if (l)
    if (l.document)
      if ((t = l.document) != null && t.mimetype) {
        const u = i(l.document.mimetype);
        if (u !== "application/vnd.js-crossword")
          return r(
            `Unsupported "document.mimetype" (${u}) Expected: application/vnd.js-crossword`
          );
        if ((o = l.document) != null && o.version) {
          const s = i(l.document.version);
          return n.test(s) ? !0 : r(`Unsupported document version (${s}) Expected: 1.0`);
        } else
          return r('Missing "document.mimetype" element');
      } else
        return r('Missing "document.mimetype" element');
    else
      return r('Missing "document" element');
  else
    return r("[crosswordDefinition] argument is undefined or null");
}
function Zt(e, n, r) {
  if (e.x < 0 || e.x >= n.width || e.y < 0 || e.y >= n.height)
    throw new Error(`Clue ${e} doesn't start in the bounds.`);
  if (r) {
    if (e.x + e.segmentLength > n.width)
      throw new Error(`Clue ${e} exceeds horizontal bounds.`);
  } else if (e.y + e.segmentLength > n.height)
    throw new Error(`Clue ${e} exceeds vertical bounds.`);
}
function Jt(e, n, r) {
  !r && e.acrossClue && (e.acrossClue.answer = oe(
    e.acrossClue.answer,
    e.acrossClueLetterIndex,
    n
  )), r && e.downClue && (e.downClue.answer = oe(
    e.downClue.answer,
    e.downClueLetterIndex,
    n
  ));
}
const eo = (e) => (n) => {
  const r = e, i = n, l = i.headNumber;
  switch (i.direction) {
    case "across":
      return r.acrossClues.find((t) => t.headNumber === l);
    case "down":
      return r.downClues.find((t) => t.headNumber === l);
    default:
      return r.acrossClues.find((t) => t.headNumber === l) || r.downClues.find((t) => t.headNumber === l);
  }
};
function no(e, n) {
  return (r) => {
    const i = Gt(r, n);
    e[n ? "acrossClues" : "downClues"].push(i), Zt(i, e, n);
    let { x: l, y: t } = i;
    for (let o = 0; o < i.segmentLength; o += 1) {
      const u = e.cells[l][t];
      u.light = !0, u[n ? "acrossClue" : "downClue"] = i, u[n ? "acrossClueLetterIndex" : "downClueLetterIndex"] = o, i.cells.push(u), zt(o, i.wordLengths) && (u[i.isAcross ? "acrossTerminator" : "downTerminator"] = !0), to(u, i, o, r.answer, n), lo(u, i, o, r.solution), ro(o, u, i), n ? l += 1 : t += 1;
    }
  };
}
function ro(e, n, r) {
  if (e === 0) {
    if (n.labelText && n.labelText !== r.headNumber)
      throw new Error(
        `Clue ${r} has a label which is inconsistent with another clue (${n.acrossClue}).`
      );
    n.labelText = r.headNumber;
  }
}
function io(e) {
  return (n) => {
    n.tailSegments = n.tailDescriptors.map(
      eo(e)
    );
    const r = [
      ...n.wordLengths,
      ...n.tailSegments.flatMap((t) => t.wordLengths)
    ];
    n.lengthText = `(${r})`;
    let i = 0;
    const l = [n, ...n.tailSegments];
    l.forEach((t) => {
      [t.headSegment] = l, i > 0 && (t.previousClueSegment = l[i - 1]), i < l.length - 1 && (t.nextClueSegment = l[i + 1]), i += 1;
    }), l[0].flatCells = l.length === 1 ? l[0].cells : (
      // Remove duplicates from intersecting multiple segments by constructing a set
      new Set(l.flatMap((t) => t.cells))
    ), n.labelText = `${[n.headNumber].concat(n.tailSegments.map((t) => t.headNumber)).join(",")}.`, n.tailSegments.forEach((t) => {
      t.lengthText = "";
    });
  };
}
function po(e, n) {
  d(fileExists/*(n)*/);
  const r = readFileSync(n, {
    encoding: "utf8",
    flag: "r"
  });
  return Mr(e, r.toString());
}
function Mr(e, n) {
  let r;
  switch (e.trim().toLowerCase()) {
    case "application/json":
      try {
        r = JSON.parse(n);
      } catch (i) {
        return x(
          `newCrosswordDefinition: [documentText] is not a simple JSON object.
Error: ${i.message}
`,
          "error"
        ), null;
      }
      break;
    case "application/yaml":
    case "application/x-yaml":
      try {
        r = It.load(n);
      } catch (i) {
        return x(
          `newCrosswordDefinition: [documentText] is not a YAML object.
Error: ${i.message}
`,
          "error"
        ), null;
      }
      break;
    default:
      return x(
        `newCrosswordDefinition: Unsupported file type: (${e})`,
        "error"
      ), null;
  }
  return Dr(r) ? r : null;
}
function Br(e, n, r, i) {
  const l = `(${e.x + 1},${e.y + 1})`, t = `[${e[i]}[${r + 1}],${e[i][r]}]`, o = `(${n.acrossClue})`, u = `[${n.acrossClue[i]},${n[i]}]`;
  return `Clue ${e} ${i} at ${l} ${t} is not coherent with previous clue ${o} ${i} ${u}.`;
}
function lo(e, n, r, i) {
  const l = " ";
  if (i) {
    if (e.solution && // We can overwrite any cells that have the default value
    e.solution !== l && e.solution !== n.solution[r])
      throw new Error(
        Br(n, e, r, "solution")
      );
    e.solution = n.solution[r];
  } else
    e.solution = l;
}
function to(e, n, r, i, l) {
  const t = " ";
  if (i) {
    const o = n.answer[r];
    if (e.answer && // We can overwrite any cells that have default value
    e.answer !== t && e.answer !== o)
      throw new Error(
        Br(n, e, r, "answer")
      );
    e.answer = o, Jt(e, e.answer, l);
  } else
    e.answer || (e.answer = t);
}
const oo = {
  eventName: "keydown",
  keyBindings: [
    {
      key: M.backspace,
      action: (e, n, r) => {
        pn(e, n, r), hn(e, r);
      }
    },
    {
      key: M.delete,
      action: (e, n, r) => {
        pn(e, n, r);
      }
    },
    {
      key: M.enter,
      action: (e, n, r) => {
        Rn(e, r);
      }
    },
    {
      key: M.tab,
      action: (e, n, r) => {
        n.shiftKey ? Jr(e, r) : Zr(e, r);
      }
    },
    {
      key: M.space,
      action: (e, n, r) => {
        n.shiftKey ? hn(e, r) : Un(e, r);
      }
    }
  ]
}, uo = {
  eventName: "keyup",
  keyBindings: [
    {
      key: M.left,
      action: (e, n, r) => {
        Pn(e, r);
      }
    },
    {
      key: M.up,
      action: (e, n, r) => {
        jn(e, r);
      }
    },
    {
      key: M.right,
      action: (e, n, r) => {
        Hn(e, r);
      }
    },
    {
      key: M.down,
      action: (e, n, r) => {
        Bn(e, r);
      }
    }
  ]
};
function mo(e, n, r) {
  const i = new fo(
    e,
    n,
    r
  );
  return i != null && i.isValid ? i : null;
}
const so = /^[a-z]$/, co = /^[a-z]$/, ao = 5;
var ie, R, ge, P, q, xe, Ce, we, le, ve, ye, Ee, G, Ae, Re, be, en, W, ae, Q, fe, Se, nn, De, Me, Te, Be, k, $, U, ee, te, _e, He, Hr, je, jr;
class fo {
  //////////////////////////
  //// Lifecycle methods
  //////////////////////////
  constructor(n, r, i) {
    //////////////////////////
    //// Private methods
    //////////////////////////
    // Accessor for document associated with DOM
    v(this, be);
    // Accessors for DOM parent/placeholder elements
    v(this, W);
    v(this, Q);
    // Common logic for CrosswordController constructor and loadCrosswordSource()
    v(this, Se);
    /**
     * **#stateChange**: Publish an event to the listeners subscribed to _onStateChange_.
     * @param {*} eventName The name of the event to be published
     * @param {*} data not used
     */
    v(this, k);
    // Flush DOM event queue before publishing event
    // Used to publish user notification events so pending events complete first.
    v(this, U);
    // Helper to publish crosswordSolved event if the crossword is solved
    v(this, te);
    // Assign event handlers to cell's input element
    v(this, He);
    // Assign keyboard event handlers to cell element
    v(this, je);
    v(this, ie, []);
    v(this, R, new dn());
    v(this, ge, void 0);
    v(this, P, void 0);
    v(this, q, { clue: null, cell: null });
    v(this, xe, void 0);
    v(this, Ce, void 0);
    v(this, we, void 0);
    v(this, le, {});
    v(this, ve, void 0);
    v(this, ye, Wr());
    v(this, Ee, []);
    v(this, G, void 0);
    v(this, Ae, !1);
    // Events published by the CrosswordController
    v(this, Re, [
      "cellRevealed",
      "clueCleaned",
      "clueIncomplete",
      "clueReset",
      "clueRevealed",
      "clueSelected",
      "clueSolved",
      "clueTested",
      "crosswordCleaned",
      "crosswordIncomplete",
      "crosswordLoaded",
      "crosswordReset",
      "crosswordRevealed",
      "crosswordSolved",
      "crosswordTested"
    ]);
    //////////////////////////
    //// Grid element helpers
    //////////////////////////
    // Helper function to retrieve corresponding cell for cellElement
    j(this, "cell", (n) => p(this, R).modelCell(n));
    // Helper function to retrieve corresponding cellElement for cell
    j(this, "cellElement", (n) => (n.light || x(`cellElement: dark cell! ${n}`, "warn"), p(this, R).cellElement(n)));
    // Helper function to set corresponding cellElement text for cell
    j(this, "setCellElementText", (n, r) => {
      d(n.light, `dark cell! ${n}`), p(this, R).cellElement(n).firstChild.nodeValue = r;
    });
    // Helper function to retrieve corresponding revealedElement for cell
    j(this, "revealedElement", (n) => {
      d(n.light, `dark cell! ${n}`);
      const r = n.labelText ? 1 : 0;
      return p(this, R).cellElement(n).children[r];
    });
    // Helper function to retrieve corresponding incorrectElement for cell
    j(this, "incorrectElement", (n) => {
      d(n.light, `dark cell! ${n}`);
      const r = n.labelText ? 2 : 1;
      return p(this, R).cellElement(n).children[r];
    });
    // Helper function for constructor
    v(this, De, () => {
      D(this, G, {
        // Reveal solution for current letter in answer. All revealed cells have
        // distinct styling which remains for the duration of the puzzle.
        // Public shaming is strictly enforced!
        "reveal-cell": this.revealCurrentCell,
        // Remove incorrect letters in the answer after testing.
        "clean-clue": this.cleanCurrentClue,
        // Clear out the answer for the current clue
        "reset-clue": this.resetCurrentClue,
        // Reveal solution for current clue
        "reveal-clue": this.revealCurrentClue,
        // Test the current clue answer against the solution. Incorrect letters
        // have distinct styling which is removed when 'cleared' or a new letter
        // entered in the cell.
        "test-clue": this.testCurrentClue,
        // Clear out all incorrect letters in the entire crossword
        "clean-crossword": this.cleanCrossword,
        // Clear out the entire crossword
        "reset-crossword": this.resetCrossword,
        // Reveal solutions for the entire crossword.
        "reveal-crossword": this.revealCrossword,
        // Test the answers for the entire crossword against the solutions
        "test-crossword": this.testCrossword
      });
    });
    // Helper function to subscribe to CrosswordController events.
    // Refer to #controllerEventNames for complete list of events.
    v(this, Me, (n, r) => {
      n.forEach((i) => {
        d(
          this.controllerEventNames.includes(i),
          `event [${i}] is not a CrosswordController event.`
        ), p(this, Ee).push(p(this, ye).subscribe(i, r));
      });
    });
    // Helper for multi-segment current clue
    v(this, Te, (n) => n && (n === this.currentClue.previousClueSegment || n === this.currentClue.nextClueSegment));
    v(this, Be, (n) => {
      const r = (s, c) => {
        c !== this.currentClue && (x(
          `Clue has changed [was ${this.currentClue}, focused ${s}] => ${c}`
        ), this.currentClue = c);
      }, [i, l, t, o, u] = [
        this.currentClue,
        n.acrossClue,
        n.downClue,
        n.acrossClueLetterIndex,
        n.downClueLetterIndex
      ];
      return [l, t].includes(this.currentClue) ? r(n, this.currentClue) : (l ? !t : t) ? r(n, l ?? t) : p(this, Te).call(this, l) ? r(n, l) : p(this, Te).call(this, t) ? r(n, t) : r(n, u === 0 && o !== 0 ? t : l), this.currentClue !== i;
    });
    x("CrosswordController constructor"), d(
      n == null ? void 0 : n.width,
      "[crosswordDefinition] argument is null/undefined or not a crossword definition"
    ), d(
      r == null ? void 0 : r.ownerDocument,
      "[domGridParentElement] argument is null/undefined or not a DOM element"
    ), d(
      !i || i.ownerDocument,
      "[domCluesParentElement] argument is not a DOM element"
    ), D(this, Ce, r), D(this, xe, i), this.setKeyboardEventBindings([oo, uo]), D(this, Ae, E(this, Se, nn).call(this, n)), this.isValid && p(this, De).call(this);
  }
  //  Completely cleans up the crossword.
  destroy() {
    var n, r;
    D(this, R, null), D(this, P, null), (n = p(this, W, ae)) == null || n.removeChild(this.gridView), (r = p(this, Q, fe)) == null || r.removeChild(this.cluesView), p(this, Ee).forEach((i) => {
      i.remove();
    }), p(this, ie).forEach((i) => {
      const { element: l, eventName: t, handler: o } = i;
      l.removeEventListener(t, o);
    });
  }
  //////////////////////////////////
  //// User EventHandler binding
  //////////////////////////////////
  // Helper function to access API event handler functions
  userEventHandler(n) {
    return x(`elementEventHandler:${n}`), d(
      p(this, G).hasOwnProperty(n),
      `[${n}] is not a CrosswordController event handler.`
    ), p(this, G)[n].bind(this);
  }
  // Helper function to bind Controller user-event-handler to webpage
  // DOM elementId.
  bindUserEventHandlerToId(n, r = "click", i = document) {
    const l = On(n, i);
    if (l) {
      const t = this.userEventHandler(n);
      l.addEventListener(r, t), p(this, ie).push({ element: l, eventName: r, handler: t });
    }
  }
  // Helper function to bind Controller user-event-handlers to a collection
  // of webpage DOM elementIds.
  bindUserEventHandlersToIds(n = this.userEventHandlerIds, r = "click", i = document) {
    n.forEach((l) => {
      this.bindUserEventHandlerToId(l, r, i);
    });
  }
  // Helper function to bind Controller user-event-handler to webpage
  // DOM element class. Using element class names rather than element Ids
  // allows us to add controller user-event-handler to more than one
  // DOM element
  bindUserEventHandlerToClass(n, r = "click", i = document) {
    Nn(n, i).forEach((t) => {
      const o = this.userEventHandler(n);
      t.addEventListener(r, o), p(this, ie).push({ element: t, eventName: r, handler: o });
    });
  }
  // Helper function to bind Controller user-event-handlers to a collection
  // of webpage DOM elementIds.
  bindUserEventHandlersToClass(n = this.userEventHandlerIds, r = "click", i = document) {
    n.forEach(
      (l) => this.bindUserEventHandlerToClass(l, r, i)
    );
  }
  ////////////////////////////////
  //// Public property accessors
  ////////////////////////////////
  get isValid() {
    return p(this, Ae);
  }
  // Accessors for public property currentCell
  get currentCell() {
    return p(this, q).cell;
  }
  set currentCell(n) {
    x(`currentCell: ${n}`);
    const r = this.currentCell;
    n !== r && (p(this, q).cell = n, this.cellElement(n).focus(), ni(this, n, r));
  }
  // Accessors for public property currentClue
  get currentClue() {
    return p(this, q).clue;
  }
  set currentClue(n) {
    const r = this.currentClue;
    n !== r && (x(`currentClue: '${n}' [currentCell ${this.currentCell}]`), p(this, q).clue = n, ei(this, n, r), this.currentClue.cells.includes(this.currentCell) || (this.currentCell = n.cells[0]), E(this, k, $).call(this, "clueSelected", n));
  }
  // Accessor for public property model
  get model() {
    return p(this, P);
  }
  // Accessor for public property gridView
  get gridView() {
    return p(this, we);
  }
  // Accessor for public property cluesView
  get cluesView() {
    return p(this, ge);
  }
  // Accessor for addEventsListener - public event publisher
  get addEventsListener() {
    return p(this, Me);
  }
  // Accessor for public property controllerEventNames
  get controllerEventNames() {
    return [...p(this, Re)];
  }
  // Accessors for public property lastMoveEvent
  get lastMoveEvent() {
    return p(this, ve);
  }
  set lastMoveEvent(n) {
    const r = n.toLowerCase();
    d(["click", "focus"].includes(r), `unknown event: ${n}`), D(this, ve, r);
  }
  // Accessor for public property userEventHandlerIds
  get userEventHandlerIds() {
    return Object.keys(p(this, G));
  }
  //////////////////////////
  //// Public methods
  //////////////////////////
  /**
   * Programmatically set the content of a crossword grid cell
   * @param {*} cellElementId The id of the associated cell DOM element
   * @param {*} character The new text content for the cell.
   */
  setGridCell(n, r) {
    x(`setCell:${n} '${r}}'`);
    const i = !0;
    Ye(
      this,
      p(this, R).modelCell(n),
      r,
      i
    );
  }
  loadCrosswordSource(n, r, i = "") {
    d(n, "[mimeType] is undefined or null"), d(r, "[crosswordSourceText] is undefined or null"), x(`loadCrosswordSource: ${n} ${i}`);
    const l = Mr(n, r);
    return l ? E(this, Se, nn).call(this, l) : (x(
      `loadCrosswordSource: invalid crossword definition "${i}"`,
      "error"
    ), !1);
  }
  setKeyboardEventBindings(n) {
    d(
      n == null ? void 0 : n.length,
      "[eventBindings] argument is empty, null or undefined."
    );
    const r = ["keydown", "keyup"];
    n.forEach((i) => {
      var t, o;
      d(
        (t = i.eventName) == null ? void 0 : t.trim(),
        'Missing or empty "eventName" property for event binding.'
      );
      const l = i.eventName.trim().toLowerCase();
      d(
        r.includes(l),
        `Binding event name "${i.eventName}" is not supported.`
      ), d(
        (o = i.keyBindings) == null ? void 0 : o.length,
        `Missing or  empty "keyBindings" array property for [${l}].`
      ), x(`setKeyboardEventBindings: Setting keyBindings for "${l}".`), p(this, le)[l] = i.keyBindings;
    });
  }
  /////////////////////////////////
  //// Public user event handlers
  /////////////////////////////////
  testCurrentClue() {
    x(`testCurrentClue:${this.currentClue}`);
    const n = !0, r = li(this, this.currentClue, n);
    return E(this, k, $).call(this, "clueTested", r), r === _.correct ? E(this, U, ee).call(this, "clueSolved", this.currentClue) : r === _.incomplete && E(this, U, ee).call(this, "clueIncomplete", this.currentClue), r;
  }
  testCrossword() {
    x("testCrossword");
    const r = ti(this, !0);
    return E(this, k, $).call(this, "crosswordTested", r), r === _.correct ? E(this, U, ee).call(this, "crosswordSolved", p(this, P)) : r === _.incomplete && E(this, U, ee).call(this, "crosswordIncomplete", p(this, P)), r;
  }
  revealCurrentCell() {
    rn(this, this.currentCell), E(this, k, $).call(this, "cellRevealed", this.currentCell), E(this, te, _e).call(this);
  }
  revealCurrentClue() {
    ri(this, this.currentClue), E(this, k, $).call(this, "clueRevealed", this.currentClue), E(this, te, _e).call(this);
  }
  revealCrossword() {
    x("revealCrossword"), ii(this), E(this, k, $).call(this, "crosswordRevealed", this.model);
  }
  resetCurrentClue() {
    ui(this, this.currentClue), E(this, k, $).call(this, "clueReset", this.currentClue);
  }
  resetCrossword() {
    x("resetCrossword"), si(this), E(this, k, $).call(this, "crosswordReset", this.model);
  }
  cleanCurrentClue() {
    ci(this, this.currentClue), E(this, k, $).call(this, "clueCleaned", this.currentClue);
  }
  cleanCrossword() {
    x("cleanCrossword"), ai(this), E(this, k, $).call(this, "crosswordCleaned", this.model);
  }
}
ie = new WeakMap(), R = new WeakMap(), ge = new WeakMap(), P = new WeakMap(), q = new WeakMap(), xe = new WeakMap(), Ce = new WeakMap(), we = new WeakMap(), le = new WeakMap(), ve = new WeakMap(), ye = new WeakMap(), Ee = new WeakMap(), G = new WeakMap(), Ae = new WeakMap(), Re = new WeakMap(), be = new WeakSet(), en = function() {
  return p(this, W, ae).ownerDocument;
}, W = new WeakSet(), ae = function() {
  return p(this, Ce);
}, Q = new WeakSet(), fe = function() {
  return p(this, xe);
}, Se = new WeakSet(), nn = function(n) {
  var i;
  const r = Wt(n);
  return r ? (this.model && (p(this, W, ae).removeChild(this.gridView), (i = p(this, Q, fe)) == null || i.removeChild(this.cluesView), D(this, R, new dn())), D(this, P, r), D(this, we, zr(
    p(this, be, en),
    this.model,
    p(this, R)
  )), p(this, R).modelCells.filter((l) => l.light).forEach((l) => {
    E(this, je, jr).call(this, l.cellElement), E(this, He, Hr).call(this, this.cellElement(l));
  }), p(this, W, ae).appendChild(this.gridView), p(this, Q, fe) && (D(this, ge, Qr(p(this, be, en), this)), p(this, Q, fe).appendChild(this.cluesView)), this.currentClue = this.model.acrossClues.headSegments[0], E(this, k, $).call(this, "crosswordLoaded", n), !0) : (x("#bindDefinition: crosswordModel creation failed", "error"), !1);
}, De = new WeakMap(), Me = new WeakMap(), Te = new WeakMap(), Be = new WeakMap(), k = new WeakSet(), $ = function(n, r) {
  x(`stateChange: ${n}`), p(this, ye).publish(n, r);
}, U = new WeakSet(), ee = function(n, r) {
  d(
    this.controllerEventNames.includes(n),
    `unknown event "${n}"`
  ), setTimeout(() => {
    E(this, k, $).call(this, n, r);
  }, ao);
}, te = new WeakSet(), _e = function() {
  x("checkSolved"), oi(this) === _.correct && E(this, U, ee).call(this, "crosswordSolved", this.model);
}, He = new WeakSet(), Hr = function(n) {
  d(n, "cellElement is null or undefined");
  const r = this;
  n.addEventListener("focus", (i) => {
    var t;
    const l = r.cell(i.target);
    x(`event:focus ${l}`), r.currentCell !== l && (r.currentCell = l), r.lastMoveEvent = "focus", p(t = r, Be).call(t, l);
  }), n.addEventListener("click", (i) => {
    const l = r.cell(i.target);
    x(`event:click ${l}`), l === r.currentCell ? r.lastMoveEvent === "click" && Rn(r, l) : r.currentCell = l, r.lastMoveEvent = "click";
  });
}, je = new WeakSet(), jr = function(n) {
  const r = this;
  Object.keys(p(r, le)).forEach((i) => {
    const l = p(r, le)[i];
    d(l, `"${i}" bindings are null or undefined.`), n.addEventListener(i, (t) => {
      const o = t.key;
      x(`event:${i} key=[${o}]`);
      const u = l.find((f) => f.key === o), s = M.name(o), c = ["left", "right", "up", "down"].includes(s);
      if (u) {
        t.preventDefault(), x(
          t.shiftKey ? `SHIFT+${s.toUpperCase()}` : s.toUpperCase()
        );
        const f = r.cell(t.target);
        u.action(r, t, f);
      } else
        c && t.preventDefault();
    });
  }), n.addEventListener("keypress", (i) => {
    var s;
    x("event:keypress"), i.preventDefault();
    const [l, t] = [r.cell(i.target), i.key], [o, u] = [
      t.toLowerCase(),
      t.toUpperCase()
    ];
    so.test(o) && (x(`Setting cell content: [${u}]`), Kn(r, i, u), ue(r.incorrectElement(l)), E(s = r, te, _e).call(s)), co.test(o) && (x("Advancing to next cell"), Un(r, l));
  });
};
const go = {
  assert: d,
  // Validate function arguments and entry conditions
  ecs: Nn,
  // DOM helper, wrapper for document.getElementByClass()
  eid: On,
  // DOM helper, wrapper for document.getElementById()
  trace: x,
  // Log information, warnings and errors to the console
  tracing: Gr
  // Console logging toggle - pass boolean 'true' to emit messages to the console.
};
export {
  fo as Controller,
  Wt as compileCrossword,
  po as convertSourceFileToDefinition,
  go as helpers,
  mo as newCrosswordController,
  Mr as newCrosswordDefinition
};
