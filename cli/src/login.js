const http = require('http');

function login(data, callback) {
  const options = {
    hostname: '127.0.0.1',
    port: 8000,
    path: '/api/token/',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': data.length
    }
  };

  const req = http.request(options, (res) => {
    if (res.statusCode == 200) {
      res.on('data', function (d) {
        callback(JSON.parse(d));
      });
    } else {
      console.log(`Incorrect username password`)
    }
    res.on('error', function (e) {
      console.log(e);
    });
  });
  req.write(data);
  req.end();
}

module.exports.login = login;
