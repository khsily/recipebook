import axios from 'axios';
import { SERVER_URL, SERVER_PORT } from '@env';

const baseURL = `${SERVER_URL}:${SERVER_PORT}/api`;

const headerFormData = { 'Content-Type': 'multipart/form-data' };
const instance = axios.create({
    baseURL: baseURL,
    timeout: 10000,
}); // axios 기본 설정 인스턴스


export const objToForm = (obj) => Object.keys(obj)
    .filter(key => (obj[key] != null))
    .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(obj[key]))
    .join('&');


class Api {
    // GET 방식 요청
    static get(url, { header } = {}) {
        return this.fetchForm(url, 'GET', header);
    }

    // POST 방식 요청
    static post(url, { header, payload = {}, multipart } = {}) {
        return this.fetchForm(url, 'POST', header, payload, multipart);
    };

    // DELETE 방식 요청
    static delete(url, { header, payload = {} } = {}) {
        return this.fetchForm(url, 'DELETE', header, payload);
    };

    // PUT 방식 요청
    static put(url, { header, payload = {}, multipart } = {}) {
        return this.fetchForm(url, 'PUT', header, payload, multipart);
    };

    static fetchForm(url, method, header, payload, multipart) {
        let headers = header;

        // 멀티파트일경우 헤더 컨텐츠 타입으로 headerFormData(multipart/form-data) 설정
        if (multipart) headers = { ...header, ...headerFormData };

        // 멀티파트인경우 요청 데이터를 FormData 객체로 감싼 후 전달
        let data = multipart ? this.createFormData(payload) : payload;
        let responseType = multipart ? 'blob' : undefined;

        // GET 요청인 경우 body로 데이터가 전달되지 않도록 data 를 undefined로 초기화
        if (method === 'GET') data = undefined;

        return new Promise((resolve, reject) => {
            instance({ url, method, headers, data, responseType })
                .then((res) => {
                    if (res.status === 200) resolve(res.data); // 요청 성공
                    else if (res.status === 404) reject(null); // 요청 실패 (NOT FOUND)
                    else reject(res.data); // 요청 실패
                }).catch((err) => { // 요청 실패
                    const defaultErr = { status: 503, msg: 'Service Unavailable' };
                    const res = err.response;
                    const data = res ? res.data : defaultErr;
                    this._onErrorListener(data);
                    reject(data);
                });
        });
    }

    // multipart 전용 폼 데이터 생성
    static createFormData(data) {
        const form = new FormData();
        for (const key in data) {
            form.append(key, data[key]);
        }
        return form;
    }

    // 에러 발생시 호출되는 콜백 메서드 등록
    static _onErrorListener = (() => { });
    static onError(callback) {
        this._onErrorListener = callback;
    }
}

export default Api;