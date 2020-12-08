const http = require('http');

async function pastchecks(access, username, callback) {
  const options = {
    hostname: '127.0.0.1',
    port: 8000,
    path: '/api/account/pastchecks/',
    method: 'GET',
  };

  const req = http.request(options, (res) => {
    if (res.statusCode == 200) {
      res.on('data', function (d) {
        let samples = JSON.parse(d).pastchecks;
        var personal_history = [], orgs_history = [];
        samples.forEach(sample => {
          if (sample.org_name == username) {
            personal_history.push({ desc: `Name: ${sample.org_name}/${sample.name} \n  File Type: ${sample.file_type} \tTimestamp: ${sample.timestamp}\n`, id: sample.id });
          } else {
            orgs_history.push({ desc: `Name: ${sample.org_name}/${sample.name} \n  File Type: ${sample.file_type} \tTimestamp: ${sample.timestamp}\n`, id: sample.id });
          }
        });
        callback(personal_history.concat(orgs_history));
      });
    } else {
      console.log(`Access Token expired - too long time, try again`)
    }
    res.on('error', function (e) {
      console.log(e);
    });
  });

  req.setHeader('Authorization', `Bearer ${access}`)

  req.end();
}

module.exports.pastchecks = pastchecks;
