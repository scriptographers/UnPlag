const inquirer = require('inquirer');

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


module.exports.auth = auth;
