// Mocha tests

var expect = require('chai').expect;
var index = require('../index');

describe('Web Server', function() {
    it('generates a string for the signup page', function() {
        var result = index.generateHTMLString('html/htmlsection-signup.html');
        expect(result).to.be.a('string');
    });

    it('generates a string for the code confirmation screen', function() {
        var result = index.generateHTMLString('html/htmlsection-confirm.html');
        expect(result).to.be.a('string');
    });

    it('generates a string for the login page', function() {
        var result = index.generateHTMLString('html/htmlsection-login.html');
        expect(result).to.be.a('string');
    });

    it('generates a string for the loading screen', function() {
        var result = index.generateHTMLString('html/htmlsection-loading.html');
        expect(result).to.be.a('string');
    });
});