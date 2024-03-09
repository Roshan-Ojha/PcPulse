import { combineReducers, configureStore } from "@reduxjs/toolkit";
import ip_sliceReducer  from './ipreducer/ipslice'
import option_slicereducer from './optionreducer/optionslice'
import toogle_slicereducer from './tooglereducer/toogleslice'

const combined_reducer = combineReducers({
    ip_reducer:ip_sliceReducer,
    option_reducer:option_slicereducer,
    toogle_reducer:toogle_slicereducer
})

 const store = configureStore({   //exported to use as provider 
    reducer:combined_reducer
})

export type RootState = ReturnType<typeof store.getState>

export default store 