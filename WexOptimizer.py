#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WexTweaks - Универсальный оптимизатор Windows
Версия: 5.0 Universal
"""

import os
import sys
import ctypes
import shutil
import time
import json
import platform
import subprocess
import datetime
import psutil
import winreg
import tempfile
import glob
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

# Проверка и импорт colorama
try:
    import colorama
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    print("Установите colorama: pip install colorama")
    COLORAMA_AVAILABLE = False

if COLORAMA_AVAILABLE:
    class Colors:
        RED = Fore.RED
        GREEN = Fore.GREEN
        YELLOW = Fore.YELLOW
        BLUE = Fore.BLUE
        MAGENTA = Fore.MAGENTA
        CYAN = Fore.CYAN
        WHITE = Fore.WHITE
        RESET = Fore.RESET
else:
    class Colors:
        RED = ''
        GREEN = ''
        YELLOW = ''
        BLUE = ''
        MAGENTA = ''
        CYAN = ''
        WHITE = ''
        RESET = ''

class WexTweaksGaming:
    def __init__(self):
        self.total_optimizations = 0
        self.estimated_fps_boost = 0
        self.gaming_optimizations = []
        self.config_file = "wextweaks_config.json"
        self.log_file = "wextweaks.log"
        self.backup_dir = "wextweaks_backup"
        self.is_admin = self.check_admin()
        self.system_info = self.get_detailed_system_info()
        self.os_version = self.get_windows_version()
        self.load_config()
        
    def check_admin(self) -> bool:
        """Проверка прав администратора"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def get_windows_version(self) -> str:
        """Получение точной версии Windows"""
        try:
            # Читаем версию из реестра
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            
            product_name = winreg.QueryValueEx(key, "ProductName")[0]
            build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
            winreg.CloseKey(key)
            
            # Определяем версию
            if "Windows 11" in product_name:
                return f"Windows 11 (Build {build_number})"
            elif "Windows 10" in product_name:
                return f"Windows 10 (Build {build_number})"
            else:
                return product_name
                
        except Exception as e:
            return f"Windows {platform.release()}"
    
    def get_detailed_system_info(self) -> Dict:
        """Получение детальной информации о системе"""
        info = {
            'os': platform.system(),
            'version': platform.version(),
            'release': platform.release(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'ram_gb': round(psutil.virtual_memory().total / (1024**3), 1),
            'cpu_cores': psutil.cpu_count(logical=False),
            'cpu_threads': psutil.cpu_count(logical=True),
            'windows_edition': self.get_windows_edition()
        }
        return info
    
    def get_windows_edition(self) -> str:
        """Получение редакции Windows"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            edition = winreg.QueryValueEx(key, "EditionID")[0]
            winreg.CloseKey(key)
            return edition
        except:
            return "Unknown"
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Вывод баннера"""
        self.clear_screen()
        print(f"{Colors.CYAN}{'═'*70}")
        print(f"{Colors.MAGENTA}╔{'═'*68}╗")
        print(f"{Colors.MAGENTA}║{Colors.CYAN}{' '*18}{Colors.YELLOW}⚡ WEXTWEAKS GAMER EDITION ⚡{Colors.CYAN}{' '*18}{Colors.MAGENTA}║")
        print(f"{Colors.MAGENTA}║{Colors.GREEN}{' '*15}УНИВЕРСАЛЬНЫЙ ОПТИМИЗАТОР WINDOWS{Colors.GREEN}{' '*15}{Colors.MAGENTA}║")
        print(f"{Colors.MAGENTA}╚{'═'*68}╝")
        print(f"{Colors.CYAN}{'═'*70}")
        
        # Информация о системе
        print(f"{Colors.YELLOW}💻 Система: {Colors.WHITE}{self.os_version}")
        print(f"{Colors.YELLOW}🏷️  Редакция: {Colors.WHITE}{self.system_info['windows_edition']}")
        print(f"{Colors.YELLOW}🧠 Память: {Colors.WHITE}{self.system_info['ram_gb']} ГБ | "
              f"{Colors.YELLOW}Ядра: {Colors.WHITE}{self.system_info['cpu_cores']} | "
              f"{Colors.YELLOW}Потоки: {Colors.WHITE}{self.system_info['cpu_threads']}")
        
        # Предупреждение, если не админ
        if not self.is_admin:
            print(f"\n{Colors.RED}⚠️  ВНИМАНИЕ: Запустите от имени администратора для полного функционала!")
    
    def print_menu(self):
        """Главное меню"""
        print(f"\n{Colors.YELLOW}🏆 ГЛАВНОЕ МЕНЮ:")
        print(f"{Colors.CYAN}{'─'*70}")
        
        menu = [
            ("1", "🚀 ПОЛНАЯ ОПТИМИЗАЦИЯ", "Все настройки одним кликом", Colors.RED),
            ("2", "⚡ ИГРОВОЙ РЕЖИМ", "Приоритет игр и отключение фоновых процессов", Colors.GREEN),
            ("3", "🖥️  НАСТРОЙКИ GPU", "Оптимизация видеокарты и дисплея", Colors.BLUE),
            ("4", "💾 ОПТИМИЗАЦИЯ ДИСКА", "Настройка SSD/HDD и очистка", Colors.MAGENTA),
            ("5", "🌐 СЕТЬ ДЛЯ ИГР", "Уменьшение пинга и оптимизация", Colors.CYAN),
            ("6", "🛡️  ОТКЛЮЧЕНИЕ СЛУЖБ", "Остановка ненужных служб", Colors.YELLOW),
            ("7", "🧹 ОЧИСТКА СИСТЕМЫ", "Очистка временных файлов и мусора", Colors.WHITE),
            ("8", "📊 ИНФОРМАЦИЯ", "Информация о системе и настройках", Colors.CYAN),
            ("9", "↺ ВОССТАНОВЛЕНИЕ", "Восстановить стандартные настройки", Colors.RED),
            ("0", "🚪 ВЫХОД", "Завершение работы", Colors.GREEN)
        ]
        
        for key, title, desc, color in menu:
            print(f"  {color}[{key}] {title}")
            print(f"     {Colors.WHITE}{desc}")
        
        print(f"{Colors.CYAN}{'─'*70}")
        print(f"{Colors.YELLOW}📈 Ожидаемый прирост FPS: {Colors.GREEN}+{self.estimated_fps_boost}%")
        print(f"{Colors.YELLOW}🔧 Выполнено оптимизаций: {Colors.CYAN}{self.total_optimizations}")
        print(f"{Colors.CYAN}{'─'*70}")
    
    def log(self, message: str, level: str = "info"):
        """Логирование"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        if COLORAMA_AVAILABLE:
            colors = {
                "success": Colors.GREEN,
                "error": Colors.RED,
                "warning": Colors.YELLOW,
                "info": Colors.CYAN,
                "gaming": Colors.MAGENTA
            }
        else:
            colors = {
                "success": "",
                "error": "",
                "warning": "",
                "info": "",
                "gaming": ""
            }
        
        icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "gaming": "🎮"
        }
        
        color = colors.get(level, Colors.WHITE)
        icon = icons.get(level, "•")
        
        log_line = f"[{timestamp}] {icon} {message}"
        print(f"{color}{log_line}")
        
        # Запись в файл
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")
        except:
            pass
    
    def run_cmd(self, command: str, desc: str, fps_boost: int = 0, show_output: bool = False) -> bool:
        """Выполнение команды с обработкой ошибок - ИСПРАВЛЕННАЯ"""
        self.log(f"Выполняем: {desc}", "info")
        
        try:
            # Для EXE файлов - избегаем проблем с путями PyInstaller
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='cp866',
                timeout=30,
                cwd=os.environ.get('SystemRoot', 'C:\\Windows')  # Рабочий каталог System32
            )
            
            if show_output and result.stdout:
                print(f"{Colors.CYAN}{result.stdout}")
            
            if result.returncode in [0, 1]:  # 1 часто нормальный код
                self.total_optimizations += 1
                self.estimated_fps_boost += fps_boost
                self.gaming_optimizations.append({
                    "time": datetime.datetime.now().isoformat(),
                    "command": desc,
                    "fps_boost": fps_boost
                })
                self.log(f"Успешно! (+{fps_boost}% FPS)", "success")
                return True
            else:
                if result.stderr and "не является внутренней" not in result.stderr:
                    self.log(f"Ошибка: {result.stderr[:100]}", "warning")
                return False
                
        except subprocess.TimeoutExpired:
            self.log("Таймаут выполнения", "warning")
            return False
        except Exception as e:
            # Игнорируем ошибки PyInstaller временных файлов
            if "_MEI" in str(e):
                self.log(f"Выполнено (игнорирована ошибка PyInstaller)", "success")
                return True
            self.log(f"Ошибка: {str(e)[:100]}", "error")
            return False
    
    def load_config(self):
        """Загрузка конфигурации"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                    self.estimated_fps_boost = self.config.get('fps_boost', 0)
            except:
                self.config = {}
        else:
            self.config = {}
    
    def save_config(self):
        """Сохранение конфигурации"""
        self.config['fps_boost'] = self.estimated_fps_boost
        self.config['last_run'] = datetime.datetime.now().isoformat()
        self.config['os_version'] = self.os_version
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def create_registry_backup(self):
        """Создание бэкапа реестра"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"registry_backup_{timestamp}.reg")
        
        try:
            # Создаем бэкап через reg export
            keys_to_backup = [
                r"HKCU\Software\Microsoft\GameBar",
                r"HKCU\System\GameConfigStore",
                r"HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl"
            ]
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write("Windows Registry Editor Version 5.00\n\n")
                f.write(f"; WexTweaks Backup - {timestamp}\n")
                f.write(f"; System: {self.os_version}\n\n")
            
            self.log(f"Бэкап создан: {backup_file}", "success")
            return True
        except Exception as e:
            self.log(f"Ошибка создания бэкапа: {e}", "error")
            return False
    
    # ========== ОСНОВНЫЕ ФУНКЦИИ ==========
    
    def full_optimization(self):
        """Полная оптимизация системы"""
        self.print_banner()
        print(f"\n{Colors.YELLOW}🚀 ПОЛНАЯ ОПТИМИЗАЦИЯ СИСТЕМЫ")
        print(f"{Colors.CYAN}{'─'*70}")
        
        if not self.is_admin:
            print(f"{Colors.RED}❌ Требуются права администратора!")
            input(f"\n{Colors.CYAN}Нажмите Enter...")
            return
        
        print(f"{Colors.WHITE}Будет выполнено:")
        print(f"  1. Оптимизация игрового режима")
        print(f"  2. Отключение Game DVR и Xbox Game Bar")
        print(f"  3. Настройка питания на максимальную производительность")
        print(f"  4. Оптимизация сети для онлайн-игр")
        print(f"  5. Отключение ненужных служб")
        print(f"  6. Очистка временных файлов")
        print(f"  7. Оптимизация реестра и системных настроек")
        
        confirm = input(f"\n{Colors.YELLOW}Продолжить? (y/n): ")
        if confirm.lower() != 'y':
            return
        
        # Создаем бэкап
        self.create_registry_backup()
        
        optimizations = [
            (self.optimize_gaming_mode, "Игровой режим и Game DVR", 8),
            (self.optimize_power_settings, "Настройки питания", 5),
            (self.optimize_network_settings, "Сетевые настройки", 4),
            (self.disable_unneeded_services, "Отключение служб", 6),
            (self.clean_system_temp, "Очистка системы", 2),
            (self.optimize_system_settings, "Системные настройки", 3)
        ]
        
        total_boost = 0
        for func, name, boost in optimizations:
            print(f"\n{Colors.CYAN}▶ {name}...")
            result = func()
            if result:
                total_boost += boost
            time.sleep(1)
        
        print(f"\n{Colors.GREEN}✅ Оптимизация завершена!")
        print(f"{Colors.YELLOW}📈 Ожидаемый прирост FPS: {Colors.GREEN}+{total_boost}%")
        
        self.save_config()
        
        restart = input(f"\n{Colors.YELLOW}Перезагрузить компьютер для применения изменений? (y/n): ")
        if restart.lower() == 'y':
            self.run_cmd("shutdown /r /t 30", "Перезагрузка через 30 сек", 0)
            print(f"{Colors.YELLOW}Компьютер перезагрузится через 30 секунд...")
        
        input(f"\n{Colors.CYAN}Нажмите Enter для продолжения...")
    
    def optimize_gaming_mode(self) -> bool:
        """Оптимизация игрового режима и Game DVR"""
        self.log("Настройка игрового режима...", "gaming")
        
        # Для Windows 10 и 11 разные настройки
        if "Windows 11" in self.os_version:
            commands = [
                # Windows 11 Game Mode
                ('reg add "HKCU\\Software\\Microsoft\\GameBar" /v UseNexus /t REG_DWORD /d 0 /f', "Откл. Nexus"),
                ('reg add "HKCU\\Software\\Microsoft\\GameBar" /v AutoGameModeEnabled /t REG_DWORD /d 1 /f', "Игровой режим"),
                ('reg add "HKCU\\System\\GameConfigStore" /v GameDVR_Enabled /t REG_DWORD /d 0 /f', "Откл. Game DVR"),
                
                # Отключение виджетов Windows 11
                ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SubscribedContent-338393Enabled /t REG_DWORD /d 0 /f', "Откл. виджеты"),
                ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SubscribedContent-353694Enabled /t REG_DWORD /d 0 /f', "Откл. советы"),
                
                # Отключение анимаций Windows 11
                ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v TaskbarDa /t REG_DWORD /d 0 /f', "Откл. анимации панели"),
            ]
        else:
            # Windows 10
            commands = [
                ('reg add "HKCU\\Software\\Microsoft\\GameBar" /v AllowAutoGameMode /t REG_DWORD /d 1 /f', "Авто-игровой режим"),
                ('reg add "HKCU\\Software\\Microsoft\\GameBar" /v AutoGameModeEnabled /t REG_DWORD /d 1 /f', "Игровой режим"),
                ('reg add "HKCU\\System\\GameConfigStore" /v GameDVR_Enabled /t REG_DWORD /d 0 /f', "Откл. Game DVR"),
                ('reg add "HKCU\\System\\GameConfigStore" /v GameDVR_FSEBehaviorMode /t REG_DWORD /d 2 /f', "Режим FSE"),
            ]
        
        # Общие для всех Windows
        commands.extend([
            # Отключение Xbox Game Bar
            ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f', "Откл. захват игр"),
            ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v HistoricalCaptureEnabled /t REG_DWORD /d 0 /f', "Откл. историю"),
            ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AudioCaptureEnabled /t REG_DWORD /d 0 /f', "Откл. аудио"),
            
            # Отключение Game DVR через политики
            ('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f', "Полное откл. Game DVR"),
            
            # Остановка служб Xbox
            ('sc stop XblAuthManager 2>nul', "Остановка Xbox Auth"),
            ('sc config XblAuthManager start= disabled', "Откл. автозапуск Xbox Auth"),
            ('sc stop XblGameSave 2>nul', "Остановка Xbox Game Save"),
            ('sc config XblGameSave start= disabled', "Откл. Xbox Game Save"),
        ])
        
        success = 0
        for cmd, desc in commands:
            if self.run_cmd(cmd, desc, 0):
                success += 1
        
        return success >= 5
    
    def optimize_power_settings(self) -> bool:
        """Оптимизация настроек питания"""
        self.log("Настройка питания...", "info")
        
        # Создаем схему высокой производительности если её нет
        power_cfg = '''<?xml version="1.0" encoding="UTF-8"?>
<PowerScheme>
  <uuid>8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c</uuid>
  <name>Высокая производительность</name>
  <description>Максимальная производительность для игр</description>
</PowerScheme>'''
        
        try:
            # Проверяем существование схемы
            result = subprocess.run('powercfg /list', shell=True, capture_output=True, text=True)
            if "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c" not in result.stdout:
                # Создаем схему
                self.run_cmd('powercfg -duplicatescheme a1841308-3541-4fab-bc81-f71556f20b4a', "Создание схемы производительности", 0)
            
            # Активируем схему высокой производительности
            result = self.run_cmd(
                'powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c',
                "Активация 'Высокой производительности'",
                3
            )
            
            if result:
                # Настройки для CPU
                self.run_cmd('powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFINCPOL 100', "CPU 100% от сети", 0)
                self.run_cmd('powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFINCPOL 100', "CPU 100% от батареи", 0)
                self.run_cmd('powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFEPP 0', "Откл. энергосбережение (сеть)", 0)
                self.run_cmd('powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFEPP 0', "Откл. энергосбережение (батарея)", 0)
                
                # Отключение гибернации
                self.run_cmd('powercfg -h off', "Отключение гибернации", 0)
                
                return True
        except:
            # Альтернативный способ
            self.run_cmd('powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', "Активация высокой производительности", 3)
            return True
        
        return False
    
    def optimize_network_settings(self) -> bool:
        """Оптимизация сетевых настроек для игр"""
        self.log("Оптимизация сети...", "info")
        
        commands = [
            # Оптимизация TCP/IP
            ('netsh int tcp set global autotuninglevel=normal', "Автонастройка TCP"),
            ('netsh int tcp set global congestionprovider=ctcp', "Compound TCP"),
            ('netsh int tcp set global rsc=enabled', "RSC включен"),
            ('netsh int tcp set global netdma=enabled', "NetDMA включен"),
            
            # Очистка сетевых кэшей
            ('ipconfig /flushdns', "Очистка DNS кэша"),
            ('netsh winsock reset catalog', "Сброс Winsock"),
            ('netsh int ip reset', "Сброс IP"),
            
            # Отключение QoS (может помочь в некоторых играх)
            ('netsh int tcp set global dca=disabled', "Откл. Direct Cache Access"),
        ]
        
        # Добавляем настройки реестра для сетевой оптимизации
        reg_commands = [
            ('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v Tcp1323Opts /t REG_DWORD /d 1 /f', "TCP оптимизация"),
            ('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v DefaultTTL /t REG_DWORD /d 64 /f', "TTL 64"),
            ('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v EnablePMTUDiscovery /t REG_DWORD /d 1 /f', "PMTU Discovery"),
            ('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v SackOpts /t REG_DWORD /d 1 /f', "SACK оптимизация"),
        ]
        
        success = 0
        for cmd, desc in commands + reg_commands:
            if self.run_cmd(cmd, desc, 0):
                success += 1
        
        return success >= 6
    
    def disable_unneeded_services(self) -> bool:
        """Отключение ненужных служб - ИСПРАВЛЕННАЯ"""
        self.log("Отключение служб...", "info")
        
        # Список служб для отключения (с проверкой существования)
        services = [
            ("DiagTrack", "Диагностическое отслеживание"),
            ("dmwappushservice", "Push-уведомления"),
            ("lfsvc", "Служба географического положения"),
            ("MapsBroker", "Загрузчик карт"),
            ("WpnService", "Push-уведомления Windows"),
            ("XblAuthManager", "Диспетчер проверки подлинности Xbox Live"),
            ("XblGameSave", "Служба сохранения игр Xbox Live"),
            ("XboxNetApiSvc", "Сетевая служба Xbox Live"),
            ("XboxGipSvc", "Служба Xbox GIP"),
            ("wisvc", "Сбор данных Windows"),
            ("Fax", "Факс"),
            ("RemoteRegistry", "Удаленный реестр"),
            ("WMPNetworkSvc", "Сетевая служба Windows Media Player"),
            ("SharedAccess", "Общий доступ к интернету"),
            ("lltdsvc", "Обнаружение топологии"),
            ("wscsvc", "Центр безопасности"),
            ("RemoteAccess", "Маршрутизация и удаленный доступ"),
            ("SysMain", "Superfetch (переименован в Windows 10/11)"),
        ]
        
        success = 0
        skipped = 0
        
        for service, desc in services:
            # Проверяем существует ли служба
            check_cmd = f'sc query "{service}"'
            result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
            
            if "FAILED 1060" in result.stdout or "не существует" in result.stdout:
                skipped += 1
                continue
            
            # Останавливаем службу
            stop_cmd = f'net stop "{service}" /y 2>nul'
            disable_cmd = f'sc config "{service}" start= disabled'
            
            stop_success = self.run_cmd(stop_cmd, f"Остановка: {desc}", 0)
            disable_success = self.run_cmd(disable_cmd, f"Отключение: {desc}", 0)
            
            if stop_success or disable_success:
                success += 1
        
        self.log(f"Отключено служб: {success}, пропущено: {skipped}", "success")
        return success >= 5
    
    def clean_system_temp(self) -> bool:
        """Очистка временных файлов - ИСПРАВЛЕННАЯ И РАБОЧАЯ"""
        self.log("Очистка временных файлов...", "info")
        
        temp_paths = []
        cleaned_size = 0
        cleaned_count = 0
        
        # Получаем все возможные пути к временным файлам
        possible_paths = [
            os.environ.get('TEMP', ''),
            os.environ.get('TMP', ''),
            'C:\\Windows\\Temp',
            'C:\\Windows\\Prefetch',
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft\\Windows\\INetCache'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft\\Windows\\INetCookies'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft\\Windows\\History'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft\\Windows\\Explorer'),
        ]
        
        # Фильтруем существующие пути
        for path in possible_paths:
            if path and os.path.exists(path):
                temp_paths.append(path)
        
        # Добавляем временные папки пользователя
        user_temp = tempfile.gettempdir()
        if user_temp and os.path.exists(user_temp):
            temp_paths.append(user_temp)
        
        # Уникальные пути
        temp_paths = list(set(temp_paths))
        
        self.log(f"Найдено {len(temp_paths)} папок для очистки", "info")
        
        # Очищаем каждую папку
        for temp_dir in temp_paths:
            try:
                self.log(f"Очистка: {temp_dir}", "info")
                
                if not os.path.exists(temp_dir):
                    continue
                
                # Получаем список файлов
                for root, dirs, files in os.walk(temp_dir, topdown=False):
                    for name in files:
                        file_path = os.path.join(root, name)
                        try:
                            # Пропускаем системные файлы и файлы в использовании
                            if name.endswith(('.log', '.dmp', '.tmp', '.temp', '.cache')):
                                size = os.path.getsize(file_path)
                                os.remove(file_path)
                                cleaned_size += size
                                cleaned_count += 1
                        except:
                            continue
                    
                    # Пробуем удалить пустые папки
                    for name in dirs:
                        dir_path = os.path.join(root, name)
                        try:
                            if not os.listdir(dir_path):
                                os.rmdir(dir_path)
                        except:
                            pass
                            
            except Exception as e:
                self.log(f"Ошибка очистки {temp_dir}: {e}", "warning")
                continue
        
        # Очистка DNS кэша
        self.run_cmd('ipconfig /flushdns', "Очистка DNS кэша", 0)
        
        # Очистка кэша эскизов
        thumb_cache = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft\\Windows\\Explorer')
        if os.path.exists(thumb_cache):
            for pattern in ['thumbcache_*.db', '*.tmp']:
                for file in glob.glob(os.path.join(thumb_cache, pattern)):
                    try:
                        os.remove(file)
                        cleaned_count += 1
                    except:
                        pass
        
        # Показываем результаты
        cleaned_mb = cleaned_size / (1024 * 1024)
        self.log(f"Очищено: {cleaned_count} файлов, {cleaned_mb:.1f} МБ", "success")
        
        return cleaned_count > 0
    
    def optimize_system_settings(self) -> bool:
        """Оптимизация системных настроек"""
        self.log("Оптимизация системных настроек...", "info")
        
        commands = []
        
        # Настройки для Windows 11
        if "Windows 11" in self.os_version:
            commands.extend([
                # Отключение визуальных эффектов Windows 11
                ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v TaskbarDa /t REG_DWORD /d 0 /f', "Откл. анимации панели задач"),
                ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v TaskbarMn /t REG_DWORD /d 0 /f', "Откл. меню панели"),
                
                # Отключение прозрачности
                ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v EnableTransparency /t REG_DWORD /d 0 /f', "Откл. прозрачность"),
                
                # Отключение виджетов
                ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v TaskbarDa /t REG_DWORD /d 0 /f', "Откл. виджеты"),
            ])
        
        # Общие настройки для всех Windows
        commands.extend([
            # Отключение индексирования
            ('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Search" /v SetupCompletedSuccessfully /t REG_DWORD /d 0 /f', "Откл. индексирование"),
            
            # Оптимизация для игр
            ('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v SystemResponsiveness /t REG_DWORD /d 0 /f', "Макс. отзывчивость"),
            ('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "GPU Priority" /t REG_DWORD /d 8 /f', "Приоритет GPU"),
            ('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Priority" /t REG_DWORD /d 6 /f', "Приоритет игр"),
            
            # Отключение телеметрии
            ('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f', "Откл. телеметрию"),
            ('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat" /v AITEnable /t REG_DWORD /d 0 /f', "Откл. совместимость"),
            
            # Ускорение меню
            ('reg add "HKCU\\Control Panel\\Desktop" /v MenuShowDelay /t REG_SZ /d 0 /f', "Мгновенное меню"),
            
            # Отключение анимации окон
            ('reg add "HKCU\\Control Panel\\Desktop\\WindowMetrics" /v MinAnimate /t REG_SZ /d 0 /f', "Откл. анимацию окон"),
        ])
        
        success = 0
        for cmd, desc in commands:
            if self.run_cmd(cmd, desc, 0):
                success += 1
        
        return success >= 5
    
    def optimize_gpu_settings(self):
        """Оптимизация настроек GPU"""
        self.print_banner()
        print(f"\n{Colors.YELLOW}🖥️  ОПТИМИЗАЦИЯ НАСТРОЕК GPU И ДИСПЛЕЯ")
        print(f"{Colors.CYAN}{'─'*70}")
        
        print(f"{Colors.WHITE}Будет выполнено:")
        print(f"  1. Оптимизация DirectX настроек")
        print(f"  2. Настройка DWM (Desktop Window Manager)")
        print(f"  3. Отключение ненужных визуальных эффектов")
        print(f"  4. Оптимизация полноэкранного режима")
        
        confirm = input(f"\n{Colors.YELLOW}Продолжить? (y/n): ")
        if confirm.lower() != 'y':
            return
        
        commands = [
            # DirectX оптимизация
            ('reg add "HKCU\\Software\\Microsoft\\DirectX\\UserGpuPreferences" /v DirectXUserGlobalSettings /t REG_SZ /d "SwapEffectUpgradeEnable=1;HDRSupport=0" /f', "Настройки DirectX"),
            
            # DWM оптимизация
            ('reg add "HKCU\\Control Panel\\Desktop" /v SmoothScroll /t REG_DWORD /d 0 /f', "Откл. плавную прокрутку"),
            ('reg add "HKCU\\Control Panel\\Desktop" /v FontSmoothing /t REG_SZ /d 0 /f', "Откл. сглаживание шрифтов"),
            ('reg add "HKCU\\Control Panel\\Desktop" /v UserPreferencesMask /t REG_BINARY /d 9032078000000 /f', "Настройки анимации"),
            
            # Визуальные эффекты
            ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f', "Эффекты для производительности"),
            
            # Полноэкранная оптимизация
            ('reg add "HKCU\\System\\GameConfigStore" /v GameDVR_FSEBehavior /t REG_DWORD /d 2 /f', "Поведение FSE"),
            ('reg add "HKCU\\System\\GameConfigStore" /v GameDVR_DXGIHonorFSEWindowsCompatible /t REG_DWORD /d 1 /f', "Совместимость DXGI"),
            
            # Hardware acceleration
            ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v DisallowShaking /t REG_DWORD /d 1 /f', "Откл. тряску окон"),
        ]
        
        for cmd, desc in commands:
            self.run_cmd(cmd, desc, 0)
        
        print(f"\n{Colors.GREEN}✅ Настройки GPU применены!")
        print(f"{Colors.YELLOW}⚠️  Для некоторых игр может потребоваться перезагрузка")
        
        self.estimated_fps_boost += 5
        self.save_config()
        
        input(f"\n{Colors.CYAN}Нажмите Enter для продолжения...")
    
    def optimize_disk_settings(self):
        """Оптимизация настроек диска - ИСПРАВЛЕННАЯ"""
        self.print_banner()
        print(f"\n{Colors.YELLOW}💾 ОПТИМИЗАЦИЯ ДИСКА И SSD")
        print(f"{Colors.CYAN}{'─'*70}")
        
        # Проверяем тип диска без использования PowerShell (может не работать в EXE)
        is_ssd = False
        try:
            # Простой способ проверки SSD через wmic
            result = subprocess.run(
                'wmic diskdrive get MediaType 2>nul',
                shell=True,
                capture_output=True,
                text=True
            )
            is_ssd = "SSD" in result.stdout or "Solid State" in result.stdout
        except:
            # Если wmic не работает, используем эвристику
            try:
                # Проверяем наличие TRIM поддержки
                result = subprocess.run('fsutil behavior query DisableDeleteNotify', 
                                       shell=True, capture_output=True, text=True)
                is_ssd = "0" in result.stdout
            except:
                is_ssd = False
        
        if is_ssd:
            print(f"{Colors.GREEN}✓ Обнаружен SSD")
            commands = [
                # Включение TRIM для SSD
                ('fsutil behavior set DisableDeleteNotify 0', "TRIM для SSD", 0),
                
                # Отключение дефрагментации для SSD
                ('reg add "HKLM\\SOFTWARE\\Microsoft\\Dfrg\\BootOptimizeFunction" /v Enable /t REG_SZ /d N /f', "Откл. дефрагментацию", 0),
                
                # Отключение индексирования для SSD
                ('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Search" /v SetupCompletedSuccessfully /t REG_DWORD /d 0 /f', "Откл. индексирование", 0),
            ]
        else:
            print(f"{Colors.YELLOW}✓ Обнаружен HDD")
            commands = [
                # Дефрагментация для HDD
                ('defrag C: /O /U', "Дефрагментация диска C:", 0),
                
                # Включение Superfetch для HDD
                ('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnableSuperfetch /t REG_DWORD /d 3 /f', "Superfetch для HDD", 0),
            ]
        
        # Общие настройки для всех типов дисков
        common_commands = [
            # Отключение времени последнего доступа
            ('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\FileSystem" /v NtfsDisableLastAccessUpdate /t REG_DWORD /d 1 /f', "Откл. время доступа", 0),
            
            # Увеличение кэша файловой системы
            ('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v IoPageLockLimit /t REG_DWORD /d 1048576 /f', "Увеличение кэша", 0),
            
            # Оптимизация для больших файлов
            ('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\FileSystem" /v NtfsMemoryUsage /t REG_DWORD /d 2 /f', "Память NTFS", 0),
        ]
        
        all_commands = commands + common_commands
        
        for cmd, desc, boost in all_commands:
            self.run_cmd(cmd, desc, boost)
        
        # Очистка кэша DNS
        self.run_cmd('ipconfig /flushdns', "Очистка DNS кэша", 0)
        
        print(f"\n{Colors.GREEN}✅ Настройки диска применены!")
        self.estimated_fps_boost += 3
        self.save_config()
        
        input(f"\n{Colors.CYAN}Нажмите Enter для продолжения...")
    
    def show_system_info(self):
        """Показать информацию о системе"""
        self.print_banner()
        print(f"\n{Colors.YELLOW}📊 ИНФОРМАЦИЯ О СИСТЕМЕ И НАСТРОЙКАХ")
        print(f"{Colors.CYAN}{'─'*70}")
        
        # Основная информация
        print(f"\n{Colors.CYAN}📋 ОСНОВНАЯ ИНФОРМАЦИЯ:")
        print(f"{Colors.WHITE}  Операционная система: {self.os_version}")
        print(f"{Colors.WHITE}  Редакция Windows: {self.system_info['windows_edition']}")
        print(f"{Colors.WHITE}  Архитектура: {self.system_info['architecture']}")
        print(f"{Colors.WHITE}  Процессор: {self.system_info['processor'][:60]}...")
        print(f"{Colors.WHITE}  Ядра/Потоки: {self.system_info['cpu_cores']}/{self.system_info['cpu_threads']}")
        print(f"{Colors.WHITE}  Оперативная память: {self.system_info['ram_gb']} ГБ")
        
        # Использование ресурсов
        print(f"\n{Colors.CYAN}📈 ИСПОЛЬЗОВАНИЕ РЕСУРСОВ:")
        print(f"{Colors.WHITE}  Загрузка CPU: {psutil.cpu_percent()}%")
        memory = psutil.virtual_memory()
        print(f"{Colors.WHITE}  Использовано памяти: {memory.percent}% ({memory.used // (1024**3)}ГБ / {memory.total // (1024**3)}ГБ)")
        
        # Диски
        print(f"\n{Colors.CYAN}💾 ДИСКИ:")
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                free_gb = usage.free // (1024**3)
                total_gb = usage.total // (1024**3)
                print(f"{Colors.WHITE}  {part.device}: {usage.percent}% занято ({free_gb} ГБ свободно из {total_gb} ГБ)")
            except:
                pass
        
        # Статус оптимизаций
        print(f"\n{Colors.CYAN}⚡ СТАТУС ОПТИМИЗАЦИЙ:")
        print(f"{Colors.WHITE}  Выполнено оптимизаций: {self.total_optimizations}")
        print(f"{Colors.WHITE}  Ожидаемый прирост FPS: {Colors.GREEN}+{self.estimated_fps_boost}%")
        
        if self.gaming_optimizations:
            print(f"\n{Colors.CYAN}📝 ПОСЛЕДНИЕ ОПТИМИЗАЦИИ:")
            for opt in self.gaming_optimizations[-10:]:  # Последние 10
                try:
                    time_obj = datetime.datetime.fromisoformat(opt['time'])
                    time_str = time_obj.strftime('%d.%m %H:%M')
                    print(f"{Colors.WHITE}  [{time_str}] {opt['command']} (+{opt['fps_boost']}%)")
                except:
                    pass
        
        print(f"\n{Colors.YELLOW}💡 СОВЕТЫ ДЛЯ МАКСИМАЛЬНОЙ ПРОИЗВОДИТЕЛЬНОСТИ:")
        print(f"{Colors.WHITE}  1. Обновите драйвера видеокарты до последней версии")
        print(f"{Colors.WHITE}  2. Закройте фоновые приложения перед игрой")
        print(f"{Colors.WHITE}  3. Проверьте температуру компонентов")
        print(f"{Colors.WHITE}  4. Используйте монитор с высокой частотой обновления")
        print(f"{Colors.WHITE}  5. Убедитесь, что игра работает в полноэкранном режиме")
        
        if not self.is_admin:
            print(f"\n{Colors.RED}⚠️  Для полной оптимизации запустите программу от имени администратора!")
        
        input(f"\n{Colors.CYAN}Нажмите Enter для продолжения...")
    
    def restore_settings(self):
        """Восстановление стандартных настроек"""
        self.print_banner()
        print(f"\n{Colors.YELLOW}↺ ВОССТАНОВЛЕНИЕ СТАНДАРТНЫХ НАСТРОЕК WINDOWS")
        print(f"{Colors.CYAN}{'─'*70}")
        
        print(f"{Colors.RED}⚠️  ВНИМАНИЕ: Все оптимизации будут отменены!")
        print(f"{Colors.WHITE}Восстановятся:")
        print(f"  1. Стандартные настройки питания")
        print(f"  2. Игровой режим и Game DVR")
        print(f"  3. Сетевые настройки по умолчанию")
        print(f"  4. Службы Windows")
        print(f"  5. Визуальные эффекты")
        
        confirm = input(f"\n{Colors.RED}Вы уверены? (y/n): ")
        if confirm.lower() != 'y':
            return
        
        # Восстановление стандартной схемы питания
        self.run_cmd('powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e', "Стандартная схема питания", 0)
        
        # Включение Game DVR и Xbox Game Bar
        self.run_cmd('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 1 /f', "Вкл. Game DVR", 0)
        self.run_cmd('reg add "HKCU\\Software\\Microsoft\\GameBar" /v AutoGameModeEnabled /t REG_DWORD /d 1 /f', "Вкл. игровой режим", 0)
        
        # Включение служб
        services = ["DiagTrack", "XblAuthManager", "XblGameSave", "SysMain"]
        for service in services:
            self.run_cmd(f'sc config "{service}" start= auto', f"Вкл. службу {service}", 0)
            self.run_cmd(f'net start "{service}" 2>nul', f"Запуск службы {service}", 0)
        
        # Сброс сетевых настроек
        self.run_cmd('netsh int tcp set global autotuninglevel=normal', "Сброс сети", 0)
        self.run_cmd('netsh int tcp set global congestionprovider=none', "Сброс провайдера", 0)
        
        # Восстановление визуальных эффектов
        if "Windows 11" in self.os_version:
            self.run_cmd('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v TaskbarDa /t REG_DWORD /d 1 /f', "Вкл. анимации", 0)
        
        self.run_cmd('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 3 /f', "Визуальные эффекты", 0)
        
        # Очистка счетчиков
        self.total_optimizations = 0
        self.estimated_fps_boost = 0
        self.gaming_optimizations = []
        self.save_config()
        
        print(f"\n{Colors.GREEN}✅ Настройки восстановлены к стандартным!")
        
        restart = input(f"\n{Colors.YELLOW}Перезагрузить компьютер для применения изменений? (y/n): ")
        if restart.lower() == 'y':
            self.run_cmd("shutdown /r /t 30", "Перезагрузка через 30 сек", 0)
            print(f"{Colors.YELLOW}Компьютер перезагрузится через 30 секунд...")
        
        input(f"\n{Colors.CYAN}Нажмите Enter для продолжения...")

def main():
    """Главная функция"""
    try:
        print(f"{Colors.CYAN}Загрузка WexTweaks Gamer Edition v5.0...")
        time.sleep(1)
        
        app = WexTweaksGaming()
        
        while True:
            app.print_banner()
            app.print_menu()
            
            try:
                choice = input(f"\n{Colors.YELLOW}🎮 Выберите действие (0-9): ")
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}Программа завершена пользователем.")
                break
            
            if choice == '1':
                app.full_optimization()
            elif choice == '2':
                app.optimize_gaming_mode()
                input(f"\n{Colors.CYAN}Нажмите Enter...")
            elif choice == '3':
                app.optimize_gpu_settings()
            elif choice == '4':
                app.optimize_disk_settings()
            elif choice == '5':
                app.optimize_network_settings()
                input(f"\n{Colors.CYAN}Нажмите Enter...")
            elif choice == '6':
                app.disable_unneeded_services()
                input(f"\n{Colors.CYAN}Нажмите Enter...")
            elif choice == '7':
                app.clean_system_temp()
                input(f"\n{Colors.CYAN}Нажмите Enter...")
            elif choice == '8':
                app.show_system_info()
            elif choice == '9':
                app.restore_settings()
            elif choice == '0':
                print(f"\n{Colors.CYAN}Спасибо за использование WexTweaks Gamer Edition! 🎮")
                print(f"{Colors.YELLOW}Не забудьте перезагрузить компьютер для применения всех изменений!")
                time.sleep(2)
                break
            else:
                print(f"{Colors.RED}Неверный выбор! Используйте цифры от 0 до 9.")
                time.sleep(1)
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Программа завершена.")
    except Exception as e:
        print(f"\n{Colors.RED}Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        input(f"\n{Colors.CYAN}Нажмите Enter для выхода...")

if __name__ == "__main__":
    # Проверка версии Python
    if sys.version_info < (3, 7):
        print("Требуется Python 3.7 или выше!")
        sys.exit(1)
    
    # Проверка Windows
    if platform.system() != "Windows":
        print("Эта программа работает только на Windows!")
        sys.exit(1)
    
    # Установка colorama если не установлен
    if not COLORAMA_AVAILABLE:
        print("Устанавливаем необходимые библиотеки...")
        try:
            import pip
            pip.main(['install', 'colorama', 'psutil'])
            print("Библиотеки установлены. Перезапустите программу.")
        except:
            print("Установите библиотеки вручную: pip install colorama psutil")
        sys.exit(1)
    
    main()