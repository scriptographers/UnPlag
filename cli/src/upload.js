const http = require('http');
const fs = require('fs');
const FormData = require('form-data');

function upload(access, file_loc, file_name, org_id, file_type) {
  const form = new FormData();

  const read_stream = fs.createReadStream(file_loc);
  form.append('plagzip', read_stream);
  form.append('name', file_name);
  form.append('org_id', org_id);
  form.append('file_type', file_type);

  const options = {
    hostname: '127.0.0.1',
    port: 8000,
    path: '/api/plagsample/upload/',
    method: 'POST',
    headers: form.getHeaders(),
  };

  const req = http.request(options, res => {
    if (res.statusCode == 401) {
      console.log('Access Token expired - too long time, try again');
    } else if (res.statusCode == 403) {
      console.log('Forbidden');
    } else if (res.statusCode == 400) {
      console.log('Bad Request');
    } else if (res.statusCode == 201) {
      console.log('Successfully upload');
    }

    res.on('error', error => {
      console.error(error);
    });
  });

  req.setHeader('Authorization', `Bearer ${access}`)

  form.getLength(function (err, length) {
    if (err) {
      this._error(err);
      return;
    }
    // add content length
    req.setHeader('Content-Length', length);
    form.pipe(req);
  }.bind(form));
}

module.exports.upload = upload;
