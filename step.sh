#!/bin/bash                                                                                                                                              
                                                                                                                                                        
git config core.hooksPath hooks
chmod +x hooks/pre-commit
                                                                                                                                                        
echo "Git hooks configured. Pre-commit checks are now active."                                                                                           
                                                                                                                                                        
Then make it executable:                                                                                                                                 
chmod +x setup.sh