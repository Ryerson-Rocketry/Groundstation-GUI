import {GETRequest} from "../Connectors/FlaskCRUD"


export class GraphModel {
    graphid: number;
    done: boolean;  
    
    constructor(graphid: number, done: boolean = false) {
        this.graphid = graphid;
        this.done = done;

        this.getInitialData(this.graphid);
    }

    getInitialData(graphid: number) {
        GETRequest("/initialize/graph/" + graphid);
    }
}

