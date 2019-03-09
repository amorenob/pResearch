SELECT hist_info.id_product, products.name, Max(hist_info.sells) - MIN(hist_info.sells) AS ventas, products.price, products.price * (Max(hist_info.sells) - MIN(hist_info.sells)) as incomes   FROM public.hist_info  INNER JOIN products
ON hist_info.id_product=products.id
GROUP BY id_product, products.name, products.price
ORDER BY incomes DESC;