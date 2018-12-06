const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

// const CASAuthentication = require('cas-authentication');
// var session = require('express-session');
var app = express();

// CAS setup
// app.use( session({
//     secret            : 'super secret key',
//     resave            : false,
//     saveUninitialized : true
// }));
//
// var cas = new CASAuthentication({
//     cas_url     : 'https://fed.princeton.edu/cas',
//     service_url : 'https://localhost:3000' // add .com
// });

// view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'Views'));

// body parser midle ware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.listen(80, () => {
  console.log("Server on line...");
});


function delete_if_exists(dir_F) {
  if (fs.existsSync(dir_F)) {
    fs.unlink(dir_F, (err) => {console.log('File Replaced');});
  }
}
//_____________________________________________________

app.get('/admin', (req, res) => {
  res.statusCode = 200;
  var areas = fs.readFileSync("questions/areas.txt", { "encoding": "utf8"});
  var discriptions = fs.readFileSync("questions/discriptions.txt", { "encoding": "utf8"});
  res.render('admin', {elements: areas, discriptions: discriptions});
});


app.post('/admin', (req, res) => {
  var Data = req.body.Data;
  var fileName = req.body.fileName;
  if(fileName.length > 30) {
    console.log("Incorrect file entery");
  } else if(! /^[a-zA-Z0-9._]+$/.test(fileName)) {
    console.log("Incorrect file entery");
  } else {
    Data = Data.replace(/,"/g, ',\n"');
    Data = Data.replace(/{/, '{\n');
    Data = Data.replace(/}/, '\n}');
    console.log(Data);
    // TODO good behavior? (delete if exists)
    delete_if_exists("adminFiles/" + fileName + '.json');
    fs.appendFile('adminFiles/'+fileName+'.json', Data, () => {console.log("Data Saved")});
  }
});

//_____________________________________________________

app.get('/user/:file', (req, res) => {
  var file = req.params.file;
  if(file.length > 30) {
    console.log("Incorrect file entery");
  } else if(! /^[a-zA-Z0-9._]+$/.test(file)) {
    console.log("Incorrect file entery");
  } else {
    res.statusCode = 200;
    try {
      var contents = fs.readFileSync("adminFiles/" + file, { "encoding": "utf8"});
      console.log(contents);
      res.render('user', {
        text: contents,
        fileName: file
      });
    } catch(err) {
      res.writeHead(200, {'Content-Type': 'text/plain'});
      res.end('Not such file, please make sure that you have the right url.');
    }
  }
});


app.post('/user', (req, res) => {
  var Data = req.body.Data;
  var fileName = req.body.fileName;
  if(fileName.length > 30) {
    fileName = prompt("The file name has to be less then 30 characters.");
  } else if(! /^[a-zA-Z0-9]+$/.test(fileName)) {
    fileName = prompt("The file name must contain only letters.");
  } else {
    Data = Data.replace(/,"/g, ',\n"');
    Data = Data.replace(/{/, '{\n');
    Data = Data.replace(/}/, '\n}');
    console.log(Data);
    delete_if_exists("userFiles/" + fileName + '.json');
    fs.appendFile('userFiles/'+fileName+'.json', Data, () => {console.log("Data Saved")})
    res.render('submitedPage');
  }
});

//_____________________________________________________
//
//app.get('/download/:file(*)',(req, res) => {
//  var file = req.params.file;
//  var fileLocation = path.join('./userFiles',file);
//  console.log(fileLocation);
//  res.download(fileLocation, file);
//});
//
//
//app.get('/library', (req, res) => {
//  fs.readdir('userFiles', (err, files) => {
//    var file_list = [];
//    files.forEach(file => {
//      file_list.push(file);
//    });
//    console.log(file_list);
//    res.render('downloads', {files: file_list});
//  });
//});
