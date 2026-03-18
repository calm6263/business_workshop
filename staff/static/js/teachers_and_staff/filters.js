// static/js/teachers_and_staff/filters.js
// ========================================

import { applyFilter } from './filterUtils.js';

let currentFilter = 'all';
let isFilterOpen = false;

export function setupFilters() {
    const filterTrigger = document.querySelector('.filter-trigger');
    const filterDropdown = document.querySelector('.filter-dropdown');
    const filterOptions = document.querySelectorAll('.filter-option');
    
    if (!filterTrigger || !filterDropdown) return;
    
    filterTrigger.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleFilterDropdown();
    });
    
    filterOptions.forEach(option => {
        option.addEventListener('click', function() {
            const filterValue = this.getAttribute('data-filter');
            selectFilter(filterValue);
            closeFilterDropdown();
        });
    });
    
    document.addEventListener('click', function(e) {
        if (isFilterOpen && 
            !filterTrigger.contains(e.target) && 
            !filterDropdown.contains(e.target)) {
            closeFilterDropdown();
        }
    });
    
    document.addEventListener('keydown', function(e) {
        if (isFilterOpen && e.key === 'Escape') {
            closeFilterDropdown();
        }
    });
}

function toggleFilterDropdown() {
    isFilterOpen = !isFilterOpen;
    const filterTrigger = document.querySelector('.filter-trigger');
    const filterDropdown = document.querySelector('.filter-dropdown');
    const filterArrow = filterTrigger.querySelector('.filter-arrow');
    
    if (isFilterOpen) {
        filterTrigger.classList.add('active');
        filterDropdown.classList.add('show');
        filterArrow.classList.add('open');
    } else {
        filterTrigger.classList.remove('active');
        filterDropdown.classList.remove('show');
        filterArrow.classList.remove('open');
    }
}

function closeFilterDropdown() {
    if (!isFilterOpen) return;
    
    isFilterOpen = false;
    const filterTrigger = document.querySelector('.filter-trigger');
    const filterDropdown = document.querySelector('.filter-dropdown');
    const filterArrow = filterTrigger.querySelector('.filter-arrow');
    
    filterTrigger.classList.remove('active');
    filterDropdown.classList.remove('show');
    filterArrow.classList.remove('open');
}

function selectFilter(filterValue) {
    if (currentFilter === filterValue) return;
    
    currentFilter = filterValue;
    const filterOptions = document.querySelectorAll('.filter-option');
    const activeOption = document.querySelector(`.filter-option[data-filter="${filterValue}"]`);
    const filterLabel = document.querySelector('.filter-label');
    
    if (activeOption) {
        filterOptions.forEach(opt => opt.classList.remove('active'));
        activeOption.classList.add('active');
        filterLabel.textContent = activeOption.querySelector('.option-text').textContent;
    }
    
    applyFilter(filterValue);
}

export function getCurrentFilter() {
    return currentFilter;
}

export function resetFilter() {
    selectFilter('all');
}