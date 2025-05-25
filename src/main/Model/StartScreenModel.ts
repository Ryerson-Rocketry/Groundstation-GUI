import {GETRequest} from "../Connectors/FlaskCRUD"
import axios from 'axios';

export class StartScreenModel {


    flaskConnectionStatus: boolean;
    status: any;

    
    constructor() {
        this.status = "";
        this.flaskConnectionStatus = true;

    }

    checkStatus() {
        GETRequest("/test").then(promise => {
            this.status = promise; 
            console.log("StartScreenModel.status " + this.status)});
    }



}

