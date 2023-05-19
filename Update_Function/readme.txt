
Update_Function 主要是是自动下载数据和清理的程序，它主要是利用一个Case类下的current对象来对表格更新，更新的工具是Case类下的各种方程。

Integrated_update.py 主要包含Case类

Case类是用来创造一个数据清理实例
	用president选择清理方式，
        如果save_mode是True，会生成每一次操作的历史文件，建议只在调试时打开. 
        如果analysis_mode是True，可以使用高级分析方程（暂时还没写）. 
        最后一步 AUTO_COMPLETE是自动完成数据生成Final
        Final文件的columns是大写的，和其它总统的Final一样
        其它中间步骤文件columns是小写的，为防止和Final窜文件
        使用起来先初始化 A=Case('Biden')
        之后用xxx功能直接用 A.xxx()就好
        
               方程功能如下
        --------------1.初步处理与储存工具---------------
        1.1 make_raw：创造原始Raw文件直接产生的DATE-TEXT表
        1.2 latest：返回最新文件的版本
        1.3 save：储存新版本到文件
        1.4 save_drop：储存最新一步中删掉的行到文件
        *** 1.5 自动更新raw文件（还没写）
        
        --------------2.文字行处理工具---------------
        
        2.1 remove_nan：删除空白行
        2.2 remove_by_texts：删除含有特定字符串的行
        2.3 remove_by_exact_texts：删除和特定字符串一样的行
        2.4 remove_ALL_CAPS：删除全部大写的行
        2.5 remove_orphan_links：删除多余的link行
        2.6 fix_orphan_links：删除多余的无主link行
        2.7 remove_links：将text列中link删除
        2.8 remove_duplicates：删除重复行
        2.9 fixtext：用str2替换行文本中的str1
        2.10 addtext：第n行文本后增加str1
        2.11 add_links：文本后增加原来应该有的link
        
        ---------------3.列生成工具---------------
        3.1 add_names_col：增加姓名列
        3.2 add_ranks_col：增加职级列
        3.3 add_titles_col：增加职称列
        3.4 add_counts：增加人数列
        3.5 add_travel_meet_kind：增加四个分类列
        3.6 add_countries_involved：增加相关国家列
        3.7 add_accom：增加陪同列
        3.8 add_topics_orgs：增加相关主题和组织列
        3.9 add_link_col：将行中link提取出来生成单列
        3.10 convertdate：将行中date改为datetime.date格式
        3.11 fixdate：用str2替换行日期列中的str1
        *** 3.12 下载link列中的link并生成content列 （还没写）
        
        -------------4.辅助工具---------------
        4.1 add_travel_info：找出旅行开始结束时间
        4.2 countries_in_it：返回文本中包含的国家
        4.3 find_lastname: 找到文本里的外交官
        4.4 find_lastname_lower：找到小写文本里的外交官
        4.5 find_lastnames：找到文本里的外交官
        4.6 topics_in_it：返回文本中包含的主题
        4.7 orgs_inv：返回文本中包含的组织
        4.8 travel_dates：识别文本中的旅行时间
        4.9 fix_dates：修好文本中的时间
        4.10 intersection：找到两个list的交集
        
        --------------5.最终生成工具---------------
        5.1 FINALIZE：把列名改好后存成final文
        5.2 AUTO_COMPLETE：自动完整清理，从Raw到Final

    	--------------6.最终生成工具---------------
    	6.1 when_who_where_what_travel 返回出访相关表格
    	6.2 strangers 返回外交活动中非美人员
    	6.3 when_who_where_what_meet 返回会面相关表格