const http = require('http');
const fs = require('fs');

function download(access, id, file_name) {
  const options = {
    hostname: '127.0.0.1',
    port: 8000,
    path: `/api/plagsample/download/${id}/`,
    method: 'GET',
  };

  const req = http.request(options, (res) => {
    if (res.statusCode == 200) {
      res.on('data', function (d) {
        arr = d.toString().split('\n');
        fs.writeFile(file_name, d, function (err) {
          if (err) throw err;
          console.log('Saved!');
        });
      });
    } else {
      console.log('File is either being processed or the upload was empty/incorrect');
    }
    res.on('error', function (e) {
      console.log(e);
    });
  });

  req.setHeader('Authorization', `Bearer ${access}`);

  req.end();
}

module.exports.download = download;
