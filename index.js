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

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

var _fs  = require("fs");
const upload = multer({});
//var upload = multer({ dest: _config.destinationDir })

// coati: future support for uploading PDFs
/*
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
*/

app.get('/', (req, res) => {
    // display default page
    const htmlsection_1 =
    `
    <h1 class="mb-3">BrainDB/SRSY/Memory Marketplace</h1>
    <h4 class="mb-3">[Subheader]</h4>
    $deckList
    <p>Get started creating cards!</p>
    <form action="/upload" method="post" enctype="application/json" style="max-width: 67%; margin: auto;">
        <table style="border-collapse: collapse; border: none;">
            <tr style="border: none;">
                <td style="border: none; width: 50%">
                    <label style="float: left">Choose a name for your deck:</label>
                </td>
                <td style="border: none;">
                    <input type="text" id="deckName" name="deckName" style="float: left;">
                </td>
            </tr>
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
                    <p>[null]</p>
                </td>
                <td style="border: none;">
                    <textarea id="myText" name="myText" rows="4" cols="50" style="float: left;"></textarea>
                </td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">
                    <button type="submit" class="btn btn-primary" style="float: left;">Generate cards</button>
                </td>
                <td style="border: none;">
                    <button type="submit" class="btn btn-primary" style="float: left;">Generate cards</button>
                </td>
            </tr>
        </table>
    </form>
    `;
    // <!--<input type="file" id="myFile" style="float: left;">-->
    // <form action="/upload" method="post" enctype="multipart/form-data" >
    // name="files"

    res.writeHead(200);
    html = fs.readFileSync('index.html');
    html = html.toString().replace('$htmlsection', htmlsection_1);

    // write the list of decks to the screen
    // first, check if they exist
    var deckString = '';
    var deckFolder = './files/decks';
    fs.readdir(deckFolder, (err, files) => {
        files.forEach(file => {
            // console.log(file);
            if (file.substring(file.length - 4) == '.csv') {
                deckString += ('<li>' + file.substring(0, file.length - 4) + '</li>');
            }
        });
      });
    
    setTimeout(function() {
        if (deckString == '') {
            deckString = '<p>You currently have no decks.</p>';
        }
        else {
            deckString = '<p>Your decks:</p>' + deckString + '<br>';
        }
        html = html.replace('$deckList', deckString);
    
        res.write(html);
        res.end();
    }, 1000);

    // res.sendFile('index.html', {root: __dirname});
});

app.post('/upload', (req, res) => {
    var textToPass;
    var deckName;
    try {
        _myText = req.body.myText;
        _deckName = req.body.deckName;
    }
    catch {
        textToPass = 'null';
        deckName = '';
    }

    // call Python script
    var dataToSend;
    // spawn new child process to call the python script
    console.log('Loading, hang tight...');
    const python = spawn(
        'python',
        ['script.py',
        '--myText',
        _myText,
        '--deckName',
        _deckName
    ]
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
})

app.listen(port, () => {
    console.log(`Now listening on port ${port}`); 
});