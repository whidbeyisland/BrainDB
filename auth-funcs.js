const aws_amplify = require('aws-amplify');
const res = require('express/lib/response');

/*
async function signUp(username, password, email) {
    const user = await aws_amplify.Auth.signUp({
            username,
            password,
            attributes: {
                email
            }
    });
    const jsonResponse = await user.json();
    if (!jsonResponse) {
        return [];
    }
    return jsonResponse;
}
*/

async function signUp(username, password, email) {
    try {
        const { user } = await aws_amplify.Auth.signUp({
            username,
            password,
            attributes: {
                email,
                //phone_number
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
/*

async function signIn(username, password) {
    //const user = await aws_amplify.Auth.signIn(username, password);
    await aws_amplify.Auth.signIn(username, password)
    .then(res => {
        console.log(res); 
        console.log(res.status);       

        if (res.status == 200) {
            return res.json();
        } else {
            console.log('got here');
            throw new Error(res.status);
        }
        
    });
    return res;
}
*/

async function signOut() {
    try {
        await aws_amplify.Auth.signOut();
    } catch (error) {
        console.log('error signing out: ', error);
    }
}

module.exports = { signUp, confirmSignUp, signIn, signOut };