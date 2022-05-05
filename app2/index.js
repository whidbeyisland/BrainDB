var port = process.env.PORT || 3000,
    http = require('http'),
    fs = require('fs'),
    html = fs.readFileSync('index.html');

var log = function(entry) {
    fs.appendFileSync('/tmp/sample-app.log', new Date().toISOString() + ' - ' + entry + '\n');
};

// initialize Express
const express = require('express');
const multer = require('multer');
const {spawn} = require('child_process');
const app = express();

var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: true }));

var _fs  = require("fs");
//var _config = require("./config");
const upload = multer({});
//var upload = multer({ dest: _config.destinationDir })

// coati: shouldn't be hardcoded as 3000, but can change that later
_handleUpload = (e) => {
    console.log('got here');
    const dataForm = new FormData();
    dataForm.append('file', e.target.files[0]);  
      axios
        .post('http://localhost:' + port + '/upload', dataForm)
        .then(res => {

        })
        .catch(err => console.log(err));      
}

app.get('/', (req, res) => {
    req.header("Content-Type", "application/json");

    // display default page
    const htmlsection_1 =
    `
    <h1 class="mb-3">BrainDB/SRSY/Memory Marketplace</h1>
    <h4 class="mb-3">[Subheader]</h4>
    <p>You currently have no decks.</p>
    <p>Get started creating cards!</p>
    <form action="/upload" method="post" enctype="multipart/form-data" >
        <table style="border-collapse: collapse; border: none; max-width: 67%; margin: auto;">
            <tr style="border: none;">
                <td style="border: none;">
                    <label style="float: left;">Start with a PDF...</label>
                </td>
                <td style="border: none;">
                    <label style="float: left;">Or paste your text here...</label>
                </td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">
                    <input type="file" id="myFile" name="files" style="float: left;">
                </td>
                <td style="border: none;">
                    <textarea id="myText" name="myText" rows="4" cols="50" style="float: left;"></textarea>
                </td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">
                    <button type="submit" class="btn btn-primary" style="float: left;" onclick="this._handleUpload">Generate cards</button>
                </td>
                <td style="border: none;">
                    <button type="submit" class="btn btn-primary" style="float: left;" onclick="this._handleUpload">Generate cards</button>
                </td>
            </tr>
        </table>
    </form>
    `;

    //res.writeHead(200);
    html = fs.readFileSync('index.html');
    html = html.toString().replace('$htmlsection', htmlsection_1);
    res.write(html);
    res.end();

    // res.sendFile('index.html', {root: __dirname});
});

app.post('/upload', (req, res) => {
    req.header("Content-Type", "application/json");

    var body = '';

    req.on('data', function(chunk) {
        body += chunk;
    });

    req.on('end', function() {




        
        // coati: handle PDF uploads --- for now, just handling text






        console.log(JSON.stringify(req.body));
        var text = req.body.myText;
        console.log(text);
        fs.writeFileSync('/files/entered-text.txt', data);


        // call Python donation script
        var dataToSend;
        // spawn new child process to call the python script
        console.log('Loading, hang tight...');
        const python = spawn(
            'python',
            ['script.py']
        );

        html = fs.readFileSync('index.html');
        const htmlsection_2 =
        `<h1 class="mb-3">Loading, hang tight...</h1>;`
        html = html.toString().replace('$htmlsection', htmlsection_2);
        res.write(html);

        // collect data from script
        python.stdout.on('data', function (data) {
            // console.log('Pipe data from python script ...');
            dataToSend = data.toString();
            console.log(dataToSend);
        });
        // in close event we are sure that stream from child process is closed
        python.on('close', (code) => {
            res.write('<script>window.location.href="/";</script>');
        });
    });
})

app.listen(port, () => {
    console.log(`Now listening on port ${port}`); 
});