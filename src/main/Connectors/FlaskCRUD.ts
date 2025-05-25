import axios from 'axios';
const serverIP = "http://127.0.0.1:5000";


export async function GETRequest(routingURL: String) {
  const { data: response } = await axios.get(serverIP + routingURL); 
  return response;
  /*axios.get(serverIP + routingURL)
  .then(function (response) {
    console.log("getting: ", response.data);
  })
  .catch(function (error) {
    console.log(error);
  });
  */
}

