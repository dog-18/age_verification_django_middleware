//import * as bundleModule from './bundle.js';
//window.bundleModule = bundleModule;
import { AppType } from './bundle.js';
//import { QRCodeGenerator } from './bundle.js';

// Receive proof data via ws from the mobile app.
// POST proof data to the /age-proof endpoint
const data = {
    proof: 'dummyProof',
    data: 'dummyData'
};

// age_proof_endpoint must be set by the caller.
fetch(age_proof_endpoint, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(data => {
    console.log('Success:', data); // Handle the response data
    // if successful, the server has set the needed cookie, so we just reload the
    // protected page
    alert("Verification successful, you will now proceed to the protected area")
    location.reload()
})
.catch((error) => {
    console.error('Error:', error); // Handle any errors
});