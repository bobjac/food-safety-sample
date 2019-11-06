var os = require('os');
var exec = require('child_process').exec,
npmVersion;

exec('npm -v',
  function (error, stdout, stderr) {
    console.log('Your npm version is '+stdout);
});

console.log('Your OS version is '+os.platform()+'-'+os.release()+os.arch());
console.log('Your nodeJS version is '+process.version);
