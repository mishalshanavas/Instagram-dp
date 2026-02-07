"""
Smart Time Management Module for Instagram DP Changer

This module implements human-like scheduling with:
- Random delays to avoid patterns
- Configurable active/sleep hours
- Smart rate limiting with jitter
- Multiple time windows support
- Weekend vs weekday schedules
- Timezone support
"""

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

# Common timezone offsets (in hours from UTC)
TIMEZONES = {
    "UTC": 0,
    "GMT": 0,
    "EST": -5,
    "EDT": -4,
    "CST": -6,
    "CDT": -5,
    "MST": -7,
    "MDT": -6,
    "PST": -8,
    "PDT": -7,
    "IST": 5.5,  # India Standard Time
    "Asia/Kolkata": 5.5,
    "JST": 9,  # Japan
    "AEST": 10,  # Australia Eastern
    "NZST": 12,  # New Zealand
    "CET": 1,  # Central European
    "EET": 2,  # Eastern European
    "BST": 1,  # British Summer Time
    "CEST": 2,  # Central European Summer Time
}


class TimeManager:
    """Manages scheduling and timing logic for DP changes"""
    
    def __init__(self, config_path: Path = None):
        # Get repository root (parent of src/)
        repo_root = Path(__file__).parent.parent
        
        if config_path is None:
            config_path = repo_root / "data" / "config.json"
        
        self.config_path = config_path
        self.config = self._load_config()
        self.last_run_file = repo_root / "data" / "last_run.txt"
        self.schedule_file = repo_root / "data" / "next_scheduled.txt"
        self.tz_offset = self._parse_timezone(self.config.get("timezone", "UTC"))
    
    def _parse_timezone(self, tz_name: str) -> float:
        """
        Parse timezone name to UTC offset in hours
        
        Args:
            tz_name: Timezone name (e.g., "IST", "Asia/Kolkata", "PST", "UTC+5.5")
        
        Returns:
            UTC offset in hours (e.g., 5.5 for IST)
        """
        # Handle UTC+X or UTC-X format
        if tz_name.upper().startswith("UTC"):
            if len(tz_name) > 3:
                try:
                    offset_str = tz_name[3:]
                    return float(offset_str)
                except ValueError:
                    logger.warning(f"Invalid UTC offset format: {tz_name}, using UTC")
                    return 0
            return 0
        
        # Look up in predefined timezones
        if tz_name in TIMEZONES:
            offset = TIMEZONES[tz_name]
            logger.info(f"Using timezone: {tz_name} (UTC{offset:+.1f})")
            return offset
        
        # Default to UTC if unknown
        logger.warning(f"Unknown timezone: {tz_name}, defaulting to UTC")
        return 0
    
    def _load_config(self) -> Dict:
        """Load configuration with defaults"""
        default_config = {
            "timezone": "Asia/Kolkata",
            "min_interval_hours": 3,
            "max_interval_hours": 4,
            "random_delay_minutes": 30,
            
            # Active hours (24-hour format)
            "weekday_windows": [
                {"start": "07:00", "end": "23:30"}
            ],
            "weekend_windows": [
                {"start": "09:00", "end": "23:30"}
            ],
            
            # Behavior settings
            "use_random_delays": True
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
                    logger.info("Loaded custom configuration")
            except Exception as e:
                logger.warning(f"Error loading config, using defaults: {e}")
        else:
            # Create default config file
            self.config_path.parent.mkdir(exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            logger.info("Created default configuration file")
        
        return default_config
    
    def _get_current_time(self) -> datetime:
        """Get current time in configured timezone"""
        utc_now = datetime.now(timezone.utc)
        # Apply timezone offset
        tz_delta = timedelta(hours=self.tz_offset)
        local_time = utc_now + tz_delta
        # Return as naive datetime (easier to work with)
        return local_time.replace(tzinfo=None)
    
    def _is_weekend(self, dt: datetime = None) -> bool:
        """Check if given datetime is weekend"""
        dt = dt or self._get_current_time()
        return dt.weekday() >= 5  # Saturday=5, Sunday=6
    
    def _parse_time(self, time_str: str) -> Tuple[int, int]:
        """Parse time string 'HH:MM' to (hour, minute)"""
        hour, minute = map(int, time_str.split(':'))
        return hour, minute
    
    def _is_within_active_windows(self, dt: datetime = None) -> Tuple[bool, str]:
        """
        Check if current time is within active windows
        
        Returns:
            Tuple of (is_active: bool, reason: str)
        """
        dt = dt or self._get_current_time()
        current_time = dt.hour * 60 + dt.minute  # Minutes since midnight
        
        # Get appropriate windows
        windows = (self.config['weekend_windows'] if self._is_weekend(dt) 
                   else self.config['weekday_windows'])
        
        for window in windows:
            start_h, start_m = self._parse_time(window['start'])
            end_h, end_m = self._parse_time(window['end'])
            
            start_minutes = start_h * 60 + start_m
            end_minutes = end_h * 60 + end_m
            
            if start_minutes <= current_time <= end_minutes:
                day_type = "weekend" if self._is_weekend(dt) else "weekday"
                return True, f"Within {day_type} active window ({window['start']}-{window['end']})"
        
        day_type = "weekend" if self._is_weekend(dt) else "weekday"
        return False, f"Outside {day_type} active windows"
    
    def _get_last_run_time(self) -> Optional[datetime]:
        """Get timestamp of last successful run"""
        if not self.last_run_file.exists():
            return None
        
        try:
            with open(self.last_run_file, 'r') as f:
                timestamp = int(f.read().strip())
                return datetime.fromtimestamp(timestamp)
        except Exception as e:
            logger.warning(f"Error reading last run time: {e}")
            return None
    
    def _get_scheduled_time(self) -> Optional[datetime]:
        """Get next scheduled run time"""
        if not self.schedule_file.exists():
            return None
        
        try:
            with open(self.schedule_file, 'r') as f:
                timestamp = int(f.read().strip())
                return datetime.fromtimestamp(timestamp)
        except Exception as e:
            logger.warning(f"Error reading scheduled time: {e}")
            return None
    
    def _save_scheduled_time(self, dt: datetime):
        """Save next scheduled run time"""
        try:
            with open(self.schedule_file, 'w') as f:
                f.write(str(int(dt.timestamp())))
            logger.info(f"Next run scheduled for: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            logger.error(f"Error saving scheduled time: {e}")
    
    def _calculate_next_run(self, from_time: datetime = None) -> datetime:
        """
        Calculate next run time with smart randomization
        
        Uses:
        - Random interval between min and max hours
        - Random delay (±30 mins by default)
        - Preferred hour weighting
        - Active window constraints
        """
        from_time = from_time or self._get_current_time()
        
        # Base interval with randomization
        min_hours = self.config['min_interval_hours']
        max_hours = self.config['max_interval_hours']
        base_interval_hours = random.uniform(min_hours, max_hours)
        
        # Add random delay if enabled
        random_delay_minutes = 0
        if self.config['use_random_delays']:
            delay_range = self.config['random_delay_minutes']
            random_delay_minutes = random.randint(-delay_range, delay_range)
        
        # Calculate next run
        next_run = from_time + timedelta(
            hours=base_interval_hours,
            minutes=random_delay_minutes
        )
        
        # Ensure it's within active windows
        next_run = self._adjust_to_active_window(next_run)
        
        return next_run
    
    def _adjust_to_active_window(self, dt: datetime) -> datetime:
        """Adjust datetime to fall within active windows"""
        is_active, _ = self._is_within_active_windows(dt)
        
        if is_active:
            return dt
        
        # If outside windows, move to start of next window
        windows = (self.config['weekend_windows'] if self._is_weekend(dt)
                   else self.config['weekday_windows'])
        
        for window in windows:
            start_h, start_m = self._parse_time(window['start'])
            window_start = dt.replace(hour=start_h, minute=start_m, second=0)
            
            if dt < window_start:
                # Add random minutes to window start (0-30 mins)
                random_offset = random.randint(0, 30)
                return window_start + timedelta(minutes=random_offset)
        
        # If past all windows today, move to first window tomorrow
        next_day = dt + timedelta(days=1)
        windows_tomorrow = (self.config['weekend_windows'] if self._is_weekend(next_day)
                           else self.config['weekday_windows'])
        
        first_window = windows_tomorrow[0]
        start_h, start_m = self._parse_time(first_window['start'])
        next_run = next_day.replace(hour=start_h, minute=start_m, second=0)
        
        # Add random offset
        random_offset = random.randint(0, 30)
        return next_run + timedelta(minutes=random_offset)
    
    def should_run_now(self, force: bool = False) -> Tuple[bool, str, Dict]:
        """
        Determine if DP should be changed now
        
        Args:
            force: Bypass all checks if True
        
        Returns:
            Tuple of (should_run: bool, reason: str, details: dict)
        """
        details = {
            "current_time": self._get_current_time().strftime('%Y-%m-%d %H:%M:%S'),
            "is_weekend": self._is_weekend(),
            "forced": force
        }
        
        if force:
            logger.info("FORCE RUN: Bypassing all time checks")
            return True, "Force run enabled", details
        
        current_time = self._get_current_time()
        
        # Check 1: Active window check
        is_active, window_reason = self._is_within_active_windows(current_time)
        details['active_window_check'] = window_reason
        
        if not is_active:
            logger.info(f"SKIP: {window_reason}")
            return False, window_reason, details
        
        # Check 2: Scheduled time check (more accurate than simple rate limiting)
        scheduled_time = self._get_scheduled_time()
        
        if scheduled_time:
            details['scheduled_time'] = scheduled_time.strftime('%Y-%m-%d %H:%M:%S')
            
            if current_time < scheduled_time:
                time_remaining = scheduled_time - current_time
                hours = int(time_remaining.total_seconds() // 3600)
                minutes = int((time_remaining.total_seconds() % 3600) // 60)
                
                reason = f"Too early - scheduled for {scheduled_time.strftime('%H:%M:%S')} ({hours}h {minutes}m remaining)"
                details['time_remaining'] = f"{hours}h {minutes}m"
                logger.info(f"SKIP: {reason}")
                return False, reason, details
        
        # Check 3: Minimum interval from last run (fallback)
        last_run = self._get_last_run_time()
        
        if last_run:
            details['last_run'] = last_run.strftime('%Y-%m-%d %H:%M:%S')
            time_since_last = current_time - last_run
            min_interval = timedelta(hours=self.config['min_interval_hours'])
            
            if time_since_last < min_interval:
                time_remaining = min_interval - time_since_last
                hours = int(time_remaining.total_seconds() // 3600)
                minutes = int((time_remaining.total_seconds() % 3600) // 60)
                
                reason = f"Rate limit - minimum {self.config['min_interval_hours']}h interval ({hours}h {minutes}m remaining)"
                details['time_remaining'] = f"{hours}h {minutes}m"
                logger.info(f"SKIP: {reason}")
                return False, reason, details
        
        # All checks passed
        logger.info("✅ All time checks passed - proceeding with DP change")
        return True, "All checks passed", details
    
    def record_successful_run(self):
        """Record successful run and schedule next one"""
        current_time = self._get_current_time()
        
        # Save last run timestamp
        try:
            with open(self.last_run_file, 'w') as f:
                f.write(str(int(current_time.timestamp())))
            logger.info(f"Recorded successful run at: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            logger.error(f"Error recording last run: {e}")
        
        # Calculate and save next scheduled run
        next_run = self._calculate_next_run(current_time)
        self._save_scheduled_time(next_run)
        
        return next_run
    
    def get_schedule_info(self) -> Dict:
        """Get human-readable schedule information"""
        current_time = self._get_current_time()
        last_run = self._get_last_run_time()
        next_run = self._get_scheduled_time()
        is_active, window_status = self._is_within_active_windows()
        
        tz_name = self.config.get("timezone", "UTC")
        tz_display = f"{tz_name} (UTC{self.tz_offset:+.1f})"
        
        info = {
            "current_time": current_time.strftime('%Y-%m-%d %H:%M:%S'),
            "timezone": tz_display,
            "is_weekend": self._is_weekend(),
            "active_window_status": window_status,
            "is_in_active_window": is_active,
            "last_run": last_run.strftime('%Y-%m-%d %H:%M:%S') if last_run else "Never",
            "next_scheduled_run": next_run.strftime('%Y-%m-%d %H:%M:%S') if next_run else "Not scheduled",
            "config": {
                "min_interval_hours": self.config['min_interval_hours'],
                "max_interval_hours": self.config['max_interval_hours'],
                "random_delay_minutes": self.config['random_delay_minutes'],
                "use_random_delays": self.config['use_random_delays']
            }
        }
        
        if last_run:
            time_since_last = current_time - last_run
            info['time_since_last_run'] = f"{int(time_since_last.total_seconds() // 3600)}h {int((time_since_last.total_seconds() % 3600) // 60)}m"
        
        if next_run and current_time < next_run:
            time_until_next = next_run - current_time
            info['time_until_next_run'] = f"{int(time_until_next.total_seconds() // 3600)}h {int((time_until_next.total_seconds() % 3600) // 60)}m"
        
        return info
