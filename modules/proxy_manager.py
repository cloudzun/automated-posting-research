"""
Proxy Manager Module
Handles proxy rotation, health checks, and connection management
"""

import random
import requests
import json
import time
from typing import List, Dict, Optional
from urllib.parse import urlparse


class ProxyManager:
    def __init__(self, config_path: str = "config/proxy_config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.current_proxy_index = 0
        self.proxy_stats = {}
        self.proxies = self._load_proxies()
        
    def _load_proxies(self) -> List[Dict]:
        """Load proxies from configuration"""
        proxies = []
        
        for provider in self.config['proxy_providers']:
            if provider['provider'] == 'custom':
                proxies.extend(provider.get('proxies', []))
            elif provider['provider'] == 'bright_data':
                # Generate Bright Data proxy URLs
                username = provider['username']
                password = provider['password']
                endpoint = provider['endpoint']
                # Format depends on Bright Data configuration
                pass
            elif provider['provider'] == 'oxylabs':
                # Generate Oxylabs proxy URLs
                username = provider['username']
                password = provider['password']
                endpoint = provider['endpoint']
                # Format depends on Oxylabs configuration
                pass
        
        # Initialize stats for each proxy
        for i, proxy in enumerate(proxies):
            self.proxy_stats[i] = {
                'success_count': 0,
                'failure_count': 0,
                'last_check': None,
                'is_working': True
            }
        
        return proxies
    
    def get_next_proxy(self) -> Optional[Dict]:
        """Get the next proxy based on rotation strategy"""
        if not self.proxies:
            return None
            
        if self.config['rotation_strategy'] == 'round_robin':
            proxy = self._get_round_robin_proxy()
        elif self.config['rotation_strategy'] == 'random':
            proxy = self._get_random_proxy()
        elif self.config['rotation_strategy'] == 'least_used':
            proxy = self._get_least_used_proxy()
        else:
            proxy = self._get_round_robin_proxy()
            
        return proxy
    
    def _get_round_robin_proxy(self) -> Optional[Dict]:
        """Get proxy using round-robin strategy"""
        working_proxies = [i for i, stat in self.proxy_stats.items() 
                          if stat['is_working']]
        
        if not working_proxies:
            return None
            
        # Find next working proxy
        original_index = self.current_proxy_index
        while True:
            if self.current_proxy_index >= len(self.proxies):
                self.current_proxy_index = 0
                
            if self.current_proxy_index in working_proxies:
                proxy = self.proxies[self.current_proxy_index].copy()
                self.current_proxy_index += 1
                return self._format_proxy(proxy)
                
            self.current_proxy_index += 1
            
            # Prevent infinite loop
            if self.current_proxy_index == original_index:
                break
                
        return None
    
    def _get_random_proxy(self) -> Optional[Dict]:
        """Get a random working proxy"""
        working_proxies = [i for i, stat in self.proxy_stats.items() 
                          if stat['is_working']]
        
        if not working_proxies:
            return None
            
        selected_idx = random.choice(working_proxies)
        proxy = self.proxies[selected_idx].copy()
        return self._format_proxy(proxy)
    
    def _get_least_used_proxy(self) -> Optional[Dict]:
        """Get the least used working proxy"""
        working_proxies = [(i, stat) for i, stat in self.proxy_stats.items() 
                          if stat['is_working']]
        
        if not working_proxies:
            return None
            
        # Sort by success count (least used first)
        sorted_proxies = sorted(working_proxies, 
                               key=lambda x: x[1]['success_count'])
        selected_idx = sorted_proxies[0][0]
        
        proxy = self.proxies[selected_idx].copy()
        return self._format_proxy(proxy)
    
    def _format_proxy(self, proxy: Dict) -> Dict:
        """Format proxy for requests library"""
        if proxy.get('username') and proxy.get('password'):
            # Authenticated proxy
            auth_str = f"{proxy['username']}:{proxy['password']}"
            proxy_url = f"{proxy['protocol']}://{auth_str}@{proxy['host']}:{proxy['port']}"
        else:
            # Simple proxy
            proxy_url = f"{proxy['protocol']}://{proxy['host']}:{proxy['port']}"
        
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def test_proxy(self, proxy: Dict, test_url: str = "https://httpbin.org/ip") -> bool:
        """Test if a proxy is working"""
        try:
            timeout = self.config.get('timeout_seconds', 10)
            response = requests.get(test_url, proxies=proxy, timeout=timeout)
            return response.status_code == 200
        except Exception as e:
            print(f"Proxy test failed: {e}")
            return False
    
    def mark_proxy_status(self, proxy: Dict, is_successful: bool):
        """Update proxy statistics"""
        # Find proxy index
        for i, p in enumerate(self.proxies):
            formatted_p = self._format_proxy(p)
            if formatted_p == proxy:
                if is_successful:
                    self.proxy_stats[i]['success_count'] += 1
                else:
                    self.proxy_stats[i]['failure_count'] += 1
                    # Mark as non-working if too many failures
                    failure_rate = (self.proxy_stats[i]['failure_count'] / 
                                  (self.proxy_stats[i]['success_count'] + 
                                   self.proxy_stats[i]['failure_count']))
                    if failure_rate > 0.5:
                        self.proxy_stats[i]['is_working'] = False
                break