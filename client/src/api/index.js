/*
postman api 문서
@link https://documenter.getpostman.com/view/2590101/UUxzCTjY
*/

import * as Category from './models/category';
import * as Ingredient from './models/ingredient';
import * as Recipe from './models/recipe';

// Api.get('test_db').then((res) => console.log(res)); connection test

export {
    Category,
    Ingredient,
    Recipe,
}