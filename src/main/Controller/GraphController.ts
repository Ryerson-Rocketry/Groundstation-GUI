import {GraphModel} from "../Model/GraphModel";
import {ChartView} from "../../renderer/components/data_display/GraphView"


export class GraphController {
    private graphModel: GraphModel;
    private graphID: number
   //private chartView:ChartView;

    constructor(graphID : number) {
        this.graphID = graphID;
        this.graphModel = new GraphModel(this.graphID);
    }

}