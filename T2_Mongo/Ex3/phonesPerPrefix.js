phonesPerPrefix = function () {
  return db.phones.aggregate([{$group: {_id: "$components.prefix", no_phones: {$sum: 1}}}, {$sort: {no_phones: -1}}])
}

