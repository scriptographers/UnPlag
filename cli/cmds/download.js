const inquirer = require('inquirer');

exports.command = 'download [save_loc]'
exports.desc = 'Download csv'
exports.builder = {}
exports.handler = function (argv) {

  require('../src/auth').auth().then((res) => {
    const data = JSON.stringify(res);

    require('../src/login').login(data,
      (login_res) => { // callback function to login
        require('../src/profile').profile(login_res.access,
          (profile_res) => { // callback function to profile
            require('../src/pastchecks').pastchecks(
              login_res.access,
              profile_res.username,
              (history) => { // callback function to pastchecks
                let sample_descs = [];
                history.forEach(sample => {
                  sample_descs.push(sample.desc)
                });

                getargs(argv, sample_descs).then(
                  (answers) => {
                    if (!('save_loc' in answers)) {
                      answers.save_loc = argv.save_loc;
                    }
                    history.forEach(sample => {
                      if (answers.desc == sample.desc) {
                        answers.id = sample.id;
                      }
                    });

                    require('../src/download').download(login_res.access, answers.id, answers.save_loc);
                  }
                );
              }
            );

          });
      });
  });
}

async function getargs(argv, sample_descs) {

  const questions = [
    {
      name: 'desc',
      type: 'list',
      message: 'Choose the upload for which the csv is to be downloaded:',
      choices: sample_descs,
      pageSize: 12,
    },
    {
      name: 'save_loc',
      type: 'input',
      message: 'Enter file location to save:',
      validate: function (value) {
        if (value.length) {
          return true;
        } else {
          return 'Please enter location of file to save.';
        }
      },
      when: function () {
        if (typeof argv.save_loc != 'string') {
          return true;
        } else {
          console.log(`Enter file location to save: ${argv.save_loc}`);
          return false;
        }
      }
    },
  ];

  return inquirer.prompt(questions);
}
