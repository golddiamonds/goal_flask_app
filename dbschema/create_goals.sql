CREATE TABLE `goals` (                                                                                                     
  `id` int(11) NOT NULL AUTO_INCREMENT,                                                                                              
  `goal` varchar(140) DEFAULT NULL,                                                                                                  
  `entered_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,                                                                       
  `priority` int(1) DEFAULT NULL,                                                                                                    
  `done_value` tinyint(1) DEFAULT '0',                                                                                               
  `subgoal` int(5) DEFAULT NULL,                                                                                                     
  `category` varchar(40) DEFAULT NULL,                                                                                               
  `trash` tinyint(1) DEFAULT '0',                                                                                                    
  `archive` tinyint(1) DEFAULT '0',                                                                                                  
  `users` varchar(15) DEFAULT NULL,                                                                                                  
  PRIMARY KEY (`id`)                                                                                                                 
)
