const aws_amplify = require('aws-amplify');
const res = require('express/lib/response');

async function signUp(username, password, email) {
    try {
        const { user } = await aws_amplify.Auth.signUp({
            username,
            password,
            attributes: {
                email
            }
        });
        console.log(user);
    } catch (error) {
        console.log('error signing up:', error);
    }
}

async function confirmSignUp(username, code) {
    try {
        console.log(await aws_amplify.Auth.confirmSignUp(username, code));
    } catch (error) {
        console.log('error confirming sign up', error);
    }
}

async function signIn(username, password) {
    try {
        const user = await aws_amplify.Auth.signIn(username, password);
        return user.attributes.sub;
        
    } catch (error) {
        console.log('error signing in', error);
        return '';
    }
}

async function signOut() {
    try {
        await aws_amplify.Auth.signOut();
    } catch (error) {
        console.log('error signing out: ', error);
    }
}

module.exports = { signUp, confirmSignUp, signIn, signOut };