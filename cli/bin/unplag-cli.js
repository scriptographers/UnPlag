#!/usr/bin/env node

require = require('esm')(module /*, options*/);
// require('../src/cli').cli(process.argv);

const http = require('http');
const inquirer = require('inquirer');
const fs = require('fs');
const FormData = require('form-data');

async function auth() {
  const questions = [
    {
      name: 'username',
      type: 'input',
      message: 'Enter your username:',
      validate: function (value) {
        if (value.length) {
          return true;
        } else {
          return 'Please enter your username or e-mail address.';
        }
      }
    },
    {
      name: 'password',
      type: 'password',
      message: 'Enter your password:',
      validate: function (value) {
        if (value.length) {
          return true;
        } else {
          return 'Please enter your password.';
        }
      }
    }
  ];
  return inquirer.prompt(questions);
}

auth().then((res) => {
  const data = JSON.stringify(res);

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

  const req = http.request(options, res => {
    console.log(`statusCode: ${res.statusCode}`)

    res.on('data', response => {
      console.log(JSON.parse(response));
      upload(JSON.parse(response).access);
    })
  });

  req.on('error', error => {
    console.error(error);
  });

  req.write(data);
  req.end();
})

function upload(access) {
  const form = new FormData();

  const read_stream = fs.createReadStream('zz.zip')
  form.append('plagzip', read_stream);
  form.append('name', 'asd');

  const options = {
    hostname: '127.0.0.1',
    port: 8000,
    path: '/api/plagsample/upload/',
    method: 'POST',
    headers: form.getHeaders(),
  };

  const req = http.request(options, res => {
    console.log(`statusCode: ${res.statusCode}`)

    res.on('data', response => {
      console.log(JSON.parse(response))
    })
  });

  req.on('error', error => {
    console.error(error);
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
