// object i want



{
  posting: ["chiavari"]
  users: [{
    username: "",
    id: 234234,
    url: "",
    followers: [{
      username: "",
      id: 2345,
      url: ""
    }, {
      username: "",
      id: 54345,
      url: ""
    }, {
      username: "",
      id: 2345,
      url: ""
    }, {
      username: "",
      id: 7990,
      url: ""
    }, {
      username: "",
      id: 2345,
      url: ""
    }],
    following: []
  }]
}



var dice = 3;
var sides = 6;
var query = `
query RollDice(user: Object!) {
  rollDice(where: user, numSides: $sides)
}
`




fetch('/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify({
      query,
      variables: {
        user: {
          friends: {
            amount: 'x => x > 3',
            edges: { nodes: { user: 'x => x === "carlos"' } }
          }
        }
      },
    })
  })
  .then(r => r.json())
  .then(data => console.log('data returned:', data));
