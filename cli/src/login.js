const http = require('http');

function login(data, callback, error) {
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
    console.log(`statusCode: ${res.statusCode}`)
    res.on('data', function (d) {
      callback(JSON.parse(d));
    });
    res.on('error', function (e) {
      error(e);
    });
  });
  req.write(data);
  req.end();
}

module.exports.login = login;
