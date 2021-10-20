/*
postman api 문서
@link https://documenter.getpostman.com/view/2590101/UUxzCTjY
*/

import Api from './config';
import * as Category from './models/category';
import * as Ingredient from './models/ingredient';

// Api.get('test_db').then((res) => console.log(res)); connection test

export {
    Category,
    Ingredient,
}