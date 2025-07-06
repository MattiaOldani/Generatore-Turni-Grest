#set align(center + horizon)
#set page(flipped: true)

#let colortheme = fuchsia

#let frame(stroke) = (
  (x, y) => (
    left: if x == 0 and y == 0 {
      0pt
    } else if x == 0 or x == 1 {
      stroke
    } else {
      stroke.lighten(50%)
    },
    right: if x == 5 {
      stroke
    },
    top: if x == 0 and y == 0 {
      0pt
    } else if y == 0 or y == 1 {
      stroke
    } else {
      stroke.lighten(50%)
    },
    bottom: if y == 3 {
      stroke
    },
  )
)

#let shading(color) = (
  (x, y) => {
    if x == 0 and y == 0 {
      none
    } else if y == 0 {
      color.lighten(25%)
    } else if calc.even(y) {
      color.lighten(75%)
    }
  }
)

#show table.cell.where(x: 0).or(table.cell.where(y: 0)): set text(weight: "bold")

#set table(inset: 10pt, align: horizon, stroke: frame(colortheme), fill: shading(colortheme))

= Turni animatori
\

#table(
  columns: (15%, 17.5%, 17.5%, 17.5%, 17.5%, 17.5%),
  inset: 10pt,
  align: horizon,
  [], [Lunedì], [Martedì], [Mercoledì], [Giovedì], [Venerdì],
