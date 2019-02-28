-- query to get number of detected objects per exposure

select cat.expnum, sum(cat.objects) as nobjects, cat.pfw_attempt_id, e.exptime,
    cat.nite
    -- fcut.t_eff, fcut.skybrightness
    from exposure e, pfw_attempt att, catalog cat 
    where att.reqnum=4083 
    -- and fcut.pfw_attempt_id=att.id 
    and att.id=cat.pfw_attempt_id 
    and cat.filetype='cat_scamp' 
    and e.expnum=cat.expnum 
    group by cat.pfw_attempt_id, cat.expnum, e.exptime, cat.nite
    order by cat.expnum; > r4083_nobjects.csv
