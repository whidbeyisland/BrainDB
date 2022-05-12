const aws_amplify = require('aws-amplify');

async function signUp(username, password, email) {
    try {
        const { user } = await aws_amplify.Auth.signUp({
            username,
            password,
            attributes: {
                email,          // optional
                //phone_number,   // optional - E.164 number convention
                // other custom attributes 
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
        console.log(user);
    } catch (error) {
        console.log('error signing in', error);
    }
}

module.exports = { signUp, confirmSignUp, signIn };