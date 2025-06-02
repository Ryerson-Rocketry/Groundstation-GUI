import { create } from 'zustand'


export interface Coordinate{
    x: number
    y: number
}

interface StartingParametersState {
  mapStartingMarkerCoordinates: Coordinate
  setStartingMarkerCoordinates: (newStartingMarkerCoordinates: Coordinate) => void
  portID: number
  setPortID: (newPortID: number) => void
}

export const useStartingParametersStore = create<StartingParametersState>((set) => ({
  mapStartingMarkerCoordinates: {x: 31.0498056, y: -103.39730555555556}, //note that this causes a trailing garbage error, likely hard
  setStartingMarkerCoordinates: (newStartingMarkerCoordinates) =>set((state) => ({ mapStartingMarkerCoordinates: newStartingMarkerCoordinates })),
  portID: 5, //note that this causes a trailing garbage error, likely hard
  setPortID: (newPortID) =>set((state) => ({ portID: newPortID }))
}))


interface GeneralParametersState {
  //actively render gui data elements
  renderGUI: boolean
  setRenderGUI: (renderState: boolean) => void
}

export const useGeneralParametersStore = create<GeneralParametersState>((set) => ({
  renderGUI: true,
  setRenderGUI: (renderState) =>set((state) => ({ renderGUI: renderState }))
}))

interface StatusState {
    radioStatus: boolean
        setRadioStatus: (radioState: boolean) => void
    flaskStatus: boolean
        setFlaskStatus: (flaskStatus: boolean) => void
}

export const useStatusStore = create<StatusState>((set) => ({
  radioStatus: false,
  setRadioStatus: (radioState) =>set((state) => ({ radioStatus: radioState })),
  flaskStatus: false,
  setFlaskStatus: (flaskStatus) =>set((state) => ({ flaskStatus: flaskStatus }))
})) 

interface MapState {
    currentGPSLocation: Coordinate
        setcurrentGPSLocation: (newGPS: Coordinate) => void
}

export const useMapStore = create<MapState>((set) => ({
  currentGPSLocation: {x: 31.94205, y: -102.204550},
  setcurrentGPSLocation: (newGPS) =>set((state) => ({ currentGPSLocation: newGPS })),
 
})) 