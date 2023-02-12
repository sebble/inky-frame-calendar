async function main(args) {
  let now = new Date();
  let isodate = now.toISOString();
  let date_time = isodate.split("T")
  let [year, month, day] = date_time[0].split('-');
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
    let nicedate = function(start, end) {
      let days = Number(end) - Number(start)
      let msg = ""
      if (start == `${year}${month}${day}`) {
        msg = "Today"
      } else
      if (start == `${year}${month}${day-1}`) {
        msg = "Yesterday"
      } else
      if (start == `${year}${month}${day+1}`) {
        msg = "Tomorrow"
      } else {
        msg = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"][(new Date(`${start.substring(0,4)}-${start.substring(4,6)}-${start.substring(6,8)}`)).getDay()]
      }
      if (days > 0) {
        msg = `${msg} +${days}`
      }
      return msg;
    }
    let events = response.split("\r\n")
      .reduce((acc,v) => {
        p = v.split(":")
        if (v == "END:VEVENT") {
          if (Number(acc.end) >= Number(`${year}${month}${day}`)) {
            acc.events.push({start:nicedate(acc.start, acc.end), start_:acc.start, end:acc.end, description:acc.description, colour:acc.colour})
          }
        }
        if (p[0] == "DTSTART;VALUE=DATE") acc.start = p[1]
        if (p[0] == "DTEND;VALUE=DATE") acc.end = p[1]
        if (p[0] == "SUMMARY") {
          acc.description = p[1]
          if (p[2]) acc.colour = colours[p[2]]
          else acc.colour = colours.TAUPE
        }
        return acc
      }, {state:"cal", start:"", start_:"", end:"", description:"", colour:colours.TAUPE, events: []})
    console.log(events)
    events.events.sort((a, b) => {return (+a.start_) - (+b.start_)})
    return events.events
  });
  return {
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(events)
  }
}
