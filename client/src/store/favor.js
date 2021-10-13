import { makeAutoObservable } from 'mobx';
import { fakeLoading } from '../utils';
import * as dummy from './dummyData';

class Favor {
    favors = [];
    isFetching = false;

    constructor() {
        makeAutoObservable(this)
    }

    // sectionList에서 사용하기 위해 추가 포맷팅 필요
    get formattedFavors() {
        return this.favors.map(v => ({
            ...v,
            data: v.data.slice(),
        })).slice();
    }

    _setFavors(favors) {
        this.favors = favors;
    }

    _setIsFetching(isFetching) {
        this.isFetching = isFetching;
    }

    async fetchList() {
        this._setIsFetching(true);

        await fakeLoading(1000);
        this._setFavors(dummy.favors.payload.data);

        this._setIsFetching(false);
    }
}

const favorStore = new Favor();
export default favorStore;

