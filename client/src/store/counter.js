import { makeAutoObservable } from 'mobx';

class Counter {
    number = 0

    constructor() {
        makeAutoObservable(this)
    }

    increase() {
        this.number++;
    }

    decrease() {
        this.number--;
    }
}

const counter = new Counter();
export default counter;

