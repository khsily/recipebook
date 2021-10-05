import { useState } from 'react';

function searchQuery(arr = [], query) {
    return arr.filter((item) => item.includes(query));
}

export function useQuerySearch(searchList = [], initialData = [], initialQuery = '') {
    const [data, setData] = useState(initialData);
    const [query, setQuery] = useState(initialQuery);

    function updateQuery(newQuery) {
        setQuery(newQuery);
        setData(searchQuery(searchList, newQuery));
    }

    return [data, query, updateQuery, setData];
}