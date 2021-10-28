SELECT * FROM combination
WHERE combination @> %(combination)s AND combination <@ %(combination)s