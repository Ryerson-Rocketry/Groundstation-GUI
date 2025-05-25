import {StartScreenModel} from "../Model/StartScreenModel";

export class StartScreenController {
    StartScreenModel: StartScreenModel;

    constructor() {
        this.StartScreenModel = new StartScreenModel();
    }

    

    checkFlaskStatus(){
        this.StartScreenModel.checkStatus();      
        return "flask status is: " + this.StartScreenModel.status;
    }

}