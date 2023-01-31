async function main(args) {
  let events = await fetch(process.env.ICS_URL).then(
    (response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.text();
  })
  .then((response) => {
    // split by line
    console.log(response)
    let colours = {
      BLACK: 0,
      WHITE: 1,
      GREEN: 2,
      BLUE: 3,
      RED: 4,
      YELLOW: 5,
      ORANGE: 6,
      TAUPE: 7,
      "": 7,
    }
    let events = response.split("\r\n")
      .reduce((acc,v) => {
        p = v.split(":", 2)
        if (v == "END:VEVENT")
          acc.events.push({start:acc.start, end:acc.end, description:acc.description, colour:acc.colour})
        if (p[0] == "DTSTART;VALUE=DATE") acc.start = p[1]
        if (p[0] == "DTEND;VALUE=DATE") acc.end = p[1]
        if (p[0] == "SUMMARY") {
          acc.description = p[1]
          if (p[2]) acc.colour = colours[p[2]]
          else acc.colour = colours.TAUPE
        }
        return acc
      }, {state:"cal", start:"", end:"", description:"", colour:colours.TAUPE, events: []})
    console.log(events)
    return events.events
  });
  return {"body": JSON.stringify({"data": events})}
}