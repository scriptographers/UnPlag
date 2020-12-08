const http = require('http');

async function profile(access, callback) {
  const options = {
    hostname: '127.0.0.1',
    port: 8000,
    path: '/api/account/profile/',
    method: 'GET',
  };

  const req = http.request(options, (res) => {
    if (res.statusCode == 200) {
      res.on('data', function (d) {
        callback(JSON.parse(d));
      });
    } else {
      console.log(`Access Token expired - too long time - maybe slow internet, try again`)
    }
    res.on('error', function (e) {
      console.log(e);
    });
  });

  req.setHeader('Authorization', `Bearer ${access}`)

  req.end();
}

module.exports.profile = profile;
