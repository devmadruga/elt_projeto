SELECT 
  * 
FROM 
    AIRBNB.DEV.DIM_LISTINGS_W_HOSTS l 
    INNER JOIN AIRBNB.DEV.FCT_REVIEWS r USING (listing_id) 
WHERE 
    l.created_at >= r.review_date