const inquirer = require('inquirer');

exports.command = 'upload [file_loc] [name]'
exports.desc = 'Upload compressed folder'
exports.builder = {}
exports.handler = function (argv) {

  require('../src/auth').auth().then((res) => {
    const data = JSON.stringify(res);

    require('../src/login').login(data,
      (login_res) => {
        require('../src/profile').profile(login_res.access,
          (token, profile_res) => {

            var org_name_list = [], org;
            for (org of profile_res.orgs) {
              org_name_list.push(org.org_name);
            }

            getargs(argv, org_name_list).then(
              (answers) => {
                if (!('file_loc' in answers)) {
                  answers.file_loc = argv.file_loc;
                }
                if (!('name' in answers)) {
                  answers.name = argv.name;
                }
                for (org of profile_res.orgs) {
                  if (org.org_name == answers.org_name) {
                    answers.org_id = org.org_id;
                  }
                }

                require('../src/upload').upload(
                  token,
                  answers.file_loc,
                  answers.name,
                  answers.org_id,
                  answers.file_type
                )
              }
            )
          });
      });
  });
}

async function getargs(argv, org_list) {

  const questions = [
    {
      name: 'file_loc',
      type: 'input',
      message: 'Enter file location:',
      validate: function (value) {
        if (value.length) {
          return true;
        } else {
          return 'Please enter location of the file to be uploaded.';
        }
      },
      when: function() {
        if (typeof argv.file_loc != 'string') {
          return true;
        } else {
          console.log(`Enter file location: ${argv.file_loc}`);
          return false;
        }
      }
    },
    {
      name: 'name',
      type: 'input',
      message: 'Enter upload name:',
      validate: function (value) {
        if (value.length) {
          return true;
        } else {
          return 'Please enter name for the upload';
        }
      },
      when: function() {
        if (typeof argv.name != 'string') {
          return true;
        } else {
          console.log(`Enter upload name: ${argv.name}`);
          return false;
        }
      }
    },
    {
      name: 'org_name',
      type: 'list',
      message: 'Enter Org location:',
      choices: org_list
    },
    {
      name: 'file_type',
      type: 'list',
      message: 'Choose file type:',
      choices: ['txt', 'cpp', 'py']
    },
  ];

  return inquirer.prompt(questions);
}
