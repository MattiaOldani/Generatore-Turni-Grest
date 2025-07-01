#set align(center + horizon)
#set page(flipped: true)

#let colortheme = maroon

#let frame(stroke) = (
  (x, y) => (
    left: if x == 0 or x == 2 {
      stroke
    } else {
      0pt
    },
    right: if x > 0 {
      stroke
    },
    top: if y < 2 {
      stroke
    } else {
      0pt
    },
    bottom: stroke,
  )
)

#let shading(color) = (
  (x, y) => {
    if y == 0 {
      color
    } else if calc.even(y) {
      color.lighten(85%)
    }
  }
)

#show table.cell.where(y: 0): set text(weight: "bold", fill: colortheme.lighten(85%))

#set table(inset: 10pt, align: horizon, stroke: frame(colortheme), fill: shading(colortheme))

= Turni animatori

#table(
  columns: (auto, auto, auto, auto, auto, auto),
  inset: 10pt,
  align: horizon,
  [], [*Lunedì*], [*Martedì*], [*Mercoledì*], [*Giovedì*], [*Venerdì*],
)
