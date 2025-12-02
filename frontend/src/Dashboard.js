// src/Dashboard.js
import React, { useState, useEffect } from 'react';

// Add this at the top - will work for both local and production
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://optotask-production.up.railway.app'
  : 'http://127.0.0.1:8000';

function Dashboard({ token, onLogout }) {
  const [currentDateTime, setCurrentDateTime] = useState(new Date());
  const [showFirstForm, setShowFirstForm] = useState(false);
  const [showSecondForm, setShowSecondForm] = useState(false);
  const [openTickets, setOpenTickets] = useState([]);

  // NEW: Ticket modal state
  const [showTicketModal, setShowTicketModal] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [modalView, setModalView] = useState('main'); // 'main', 'postpone', 'referral'

  // NEW: Archive search
  const [archiveSearch, setArchiveSearch] = useState('');
  const [archiveResults, setArchiveResults] = useState([]);

  // Form state - First dropdown
  const [customerNo, setCustomerNo] = useState('');
  const [initials, setInitials] = useState('');
  const [fields, setFields] = useState(false);
  const [iops, setIops] = useState(false);
  const [scans, setScans] = useState(false);
  const [referral, setReferral] = useState(false);

  // Form state - Second dropdown
  const [fieldType, setFieldType] = useState('');
  const [iopNotes, setIopNotes] = useState('');
  const [scanType, setScanType] = useState('');
  const [referralReason, setReferralReason] = useState('');
  const [notes, setNotes] = useState('');

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentDateTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Load open tickets on mount
  useEffect(() => {
    loadOpenTickets();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadOpenTickets = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tickets/open`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setOpenTickets(data);
      }
    } catch (error) {
      console.error('Failed to load tickets:', error);
    }
  };

  const formatDateTime = (date) => {
    return date.toLocaleString('en-GB', {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const handleFirstFormSubmit = (e) => {
    e.preventDefault();
    setShowFirstForm(false);
    setShowSecondForm(true);
  };

  const handleSecondFormSubmit = async (e) => {
    e.preventDefault();

    const patientData = {
      idx: parseInt(customerNo),
      initial: initials,
      fields: fields,
      pressures: iops,  // Backend expects 'pressures'
      scans: scans,
      referral: referral,
      notes: notes
    };

    try {
      const response = await fetch(`${API_BASE_URL}/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(patientData)
      });

      if (response.ok) {
        // Reset form
        setCustomerNo('');
        setInitials('');
        setFields(false);
        setIops(false);
        setScans(false);
        setReferral(false);
        setFieldType('');
        setIopNotes('');
        setScanType('');
        setReferralReason('');
        setNotes('');
        setShowSecondForm(false);

        // Reload tickets
        loadOpenTickets();
      } else {
        alert('Failed to create patient');
      }
    } catch (error) {
      console.error('Error creating patient:', error);
      alert('Error creating patient');
    }
  };

  const handleCancelFirstForm = () => {
    setShowFirstForm(false);
    setCustomerNo('');
    setInitials('');
    setFields(false);
    setIops(false);
    setScans(false);
    setReferral(false);
  };

  const handleCancelSecondForm = () => {
    setShowSecondForm(false);
    setFieldType('');
    setIopNotes('');
    setScanType('');
    setReferralReason('');
    setNotes('');
  };

  // NEW: Open ticket modal
  const handleTicketClick = (ticket) => {
    setSelectedTicket(ticket);
    setShowTicketModal(true);
    setModalView('main');
  };

  // NEW: Close ticket (archive it)
  const handleCloseTicket = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${selectedTicket.idx}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        setShowTicketModal(false);
        setSelectedTicket(null);
        loadOpenTickets();
      }
    } catch (error) {
      console.error('Failed to close ticket:', error);
    }
  };

  // NEW: Update ticket with task completion status
  const handleUpdateTicket = async (updates) => {
    try {
      const response = await fetch(`${API_BASE_URL}/update/${selectedTicket.idx}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updates)
      });

      if (response.ok) {
        loadOpenTickets();
        setShowTicketModal(false);
        setSelectedTicket(null);
      }
    } catch (error) {
      console.error('Failed to update ticket:', error);
    }
  };

  // NEW: Postpone ticket
  const handlePostpone = async (date) => {
      await handleUpdateTicket({
      fields_result: selectedTicket.fields_result,      // ADD THIS
      pressures_result: selectedTicket.pressures_result, // ADD THIS
      scans_result: selectedTicket.scans_result,        // ADD THIS
      notes: selectedTicket.notes,
      referral: selectedTicket.referral,
      referral_sent: selectedTicket.referral_sent,
      review_date: date,
      ticket_status: 'postponed'
    });
  };

  // NEW: Mark referral as sent
  const handleReferralSent = async () => {
    await handleUpdateTicket({
      referral_sent: true,
      referral_sent_date: new Date().toISOString()
    });
  };

  // NEW: Archive search
  const handleArchiveSearch = async () => {
    if (!archiveSearch.trim()) return;

    try {
      const response = await fetch(`${API_BASE_URL}/search_archive/${archiveSearch}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setArchiveResults([data]);
      } else {
        setArchiveResults([]);
        alert('Patient not found');
      }
    } catch (error) {
      console.error('Archive search failed:', error);
    }
  };

  return (
    <div className="dashboard">
      {/* Date and Time */}
      <div className="date-time-display">
        {formatDateTime(currentDateTime)}
      </div>

      {/* Logout Button */}
      <button onClick={onLogout} className="logout-btn-dashboard">
        Logout
      </button>

      {/* Plus Button */}
      {!showFirstForm && !showSecondForm && (
        <button
          className="plus-button"
          onClick={() => setShowFirstForm(true)}
        >
          +
        </button>
      )}

      {/* First Dropdown Form */}
      {showFirstForm && (
        <div className="form-overlay">
          <form onSubmit={handleFirstFormSubmit} className="dropdown-form first-form">
            <div className="form-row">
              <input
                type="number"
                placeholder="Customer No"
                value={customerNo}
                onChange={(e) => setCustomerNo(e.target.value)}
                required
              />
              <input
                type="text"
                placeholder="Initials"
                value={initials}
                onChange={(e) => setInitials(e.target.value)}
                maxLength="3"
                required
              />
            </div>

            <div className="checkbox-row">
              <label className="checkbox-label" style={{color: '#333'}}>
                Fields {fields ? '✓' : '✗'}
                <input
                  type="checkbox"
                  checked={fields}
                  onChange={(e) => setFields(e.target.checked)}
                />
              </label>

              <label className="checkbox-label" style={{color: '#333'}}>
                IOPs {iops ? '✓' : '✗'}
                <input
                  type="checkbox"
                  checked={iops}
                  onChange={(e) => setIops(e.target.checked)}
                />
              </label>

              <label className="checkbox-label" style={{color: '#333'}}>
                Scans/Pics {scans ? '✓' : '✗'}
                <input
                  type="checkbox"
                  checked={scans}
                  onChange={(e) => setScans(e.target.checked)}
                />
              </label>

              <label className="checkbox-label" style={{color: '#333'}}>
                Referral {referral ? '✓' : '✗'}
                <input
                  type="checkbox"
                  checked={referral}
                  onChange={(e) => setReferral(e.target.checked)}
                />
              </label>
            </div>

            <div className="form-buttons">
              <button type="button" onClick={handleCancelFirstForm} className="cancel-btn">
                Cancel
              </button>
              <button type="submit" className="submit-btn">
                Next
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Second Dropdown Form */}
      {showSecondForm && (
        <div className="form-overlay active">
          <form onSubmit={handleSecondFormSubmit} className="dropdown-form second-form">
            <h3 style={{marginBottom: '20px', color: '#333'}}>Add Details for Selected Tasks</h3>

            {fields && (
              <div className="form-group">
                <label>Field Type</label>
                <select value={fieldType} onChange={(e) => setFieldType(e.target.value)}>
                  <option value="">Select field type</option>
                  <option value="C40">C40</option>
                  <option value="24-2">24-2</option>
                  <option value="FDT">FDT</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            )}

            {iops && (
              <div className="form-group">
                <label>IOP Notes (optional)</label>
                <input
                  type="text"
                  placeholder="e.g., 16mmHg normal"
                  value={iopNotes}
                  onChange={(e) => setIopNotes(e.target.value)}
                />
              </div>
            )}

            {scans && (
              <div className="form-group">
                <label>Scan Type</label>
                <select value={scanType} onChange={(e) => setScanType(e.target.value)}>
                  <option value="">Select scan type</option>
                  <option value="OCT">OCT</option>
                  <option value="Pictures">Pictures</option>
                  <option value="Both">Both</option>
                </select>
              </div>
            )}

            {referral && (
              <div className="form-group">
                <label>Referral Reason (optional)</label>
                <input
                  type="text"
                  placeholder="Why is referral needed?"
                  value={referralReason}
                  onChange={(e) => setReferralReason(e.target.value)}
                />
              </div>
            )}

            <div className="form-group">
              <label>General Notes</label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Add any notes..."
                rows="3"
              />
            </div>

            <div className="form-buttons">
              <button type="button" onClick={handleCancelSecondForm} className="cancel-btn">
                Back
              </button>
              <button type="submit" className="submit-btn">
                Create Patient
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Open Tickets */}
      <div className="tickets-container">
        {openTickets.map((ticket) => (
          <div key={ticket.idx} className="ticket-bar" onClick={() => handleTicketClick(ticket)}>
            <div className="ticket-info">
              <span className="ticket-customer">{ticket.initial.toUpperCase()} </span>
              <span className="ticket-initials">{ticket.idx}</span>
            </div>
            <div className="ticket-tasks">
              {ticket.referral && !ticket.referral_sent ? (
                <span className="task-referral-urgent">REFERRAL ⚠️</span>
              ) : (
                <>
                  <span className={ticket.fields ? 'task-active' : 'task-inactive'}>Fields</span>
                  <span className={ticket.pressures ? 'task-active' : 'task-inactive'}>IOPs</span>
                  <span className={ticket.scans ? 'task-active' : 'task-inactive'}>Scans</span>
                  <span className={ticket.referral ? 'task-active' : 'task-inactive'}>Referral</span>
                </>
              )}
            </div>
            {ticket.notes && (
              <div className="ticket-notes">{ticket.notes}</div>
            )}
          </div>
        ))}
      </div>

      {/* Archive Search Bar */}
      <div className="archive-search">
        <input
          type="text"
          placeholder="🔍 Search Archive by Customer Number..."
          className="archive-search-input"
          value={archiveSearch}
          onChange={(e) => setArchiveSearch(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleArchiveSearch()}
        />
        <button onClick={handleArchiveSearch} className="archive-search-btn">
          Search
        </button>
      </div>

      {/* Archive Results */}
      {archiveResults.length > 0 && (
          <div className="archive-results">
            <h3>Archive Results</h3>
            {archiveResults.map((ticket) => (
              <div key={ticket.idx} className="ticket-bar">
                <div className="ticket-info">
                  <span className="ticket-customer">{ticket.initial.toUpperCase()} </span>
                  <span className="ticket-initials">{ticket.idx}</span>
                  <button
                    className="audit-btn"
                    onClick={() => alert(
                      `📊 Patient Audit:\n\n` +
                      `Created: ${new Date(ticket.created_at).toLocaleString()}\n` +
                      `Completed: ${ticket.closed_date ? new Date(ticket.closed_date).toLocaleString() : 'Not completed'}\n` +
                      `Tasks Completed:\n` +
                      `- Fields: ${ticket.fields_result || 'Not done'}\n` +
                      `- IOPs: ${ticket.pressures_result || 'Not done'}\n` +
                      `- Scans: ${ticket.scans_result || 'Not done'}\n` +
                      `Referral Sent: ${ticket.referral_sent ? 'Yes' : 'No'}`
                    )}
                  >
                    📊 Audit
                  </button>
                </div>
                <div className="ticket-tasks">
                  <span className={ticket.fields ? 'task-active' : 'task-inactive'}>Fields</span>
                  <span className={ticket.pressures ? 'task-active' : 'task-inactive'}>IOPs</span>
                  <span className={ticket.scans ? 'task-active' : 'task-inactive'}>Scans</span>
                  <span className={ticket.referral ? 'task-active' : 'task-inactive'}>Referral</span>
                </div>
                {ticket.notes && (
                  <div className="ticket-notes">{ticket.notes}</div>
                )}
              </div>
            ))}
          </div>
        )}

      {/* Ticket Modal */}
      {showTicketModal && selectedTicket && (
        <div className="form-overlay" onClick={() => setShowTicketModal(false)}>
          <div className="ticket-modal" onClick={(e) => e.stopPropagation()}>
            <h2>Patient {selectedTicket.initial.toUpperCase()} - {selectedTicket.idx}</h2>

            {modalView === 'main' && (
              <>
                <div className="modal-section">
                  <h3>Mark Tasks as Complete</h3>
                  {selectedTicket.fields && (
                    <div className="task-check">
                      <label>
                        <input
                          type="checkbox"
                          checked={selectedTicket.fields_result === 'completed'}
                          onChange={(e) => {
                            const updatedTicket = {...selectedTicket, fields_result: e.target.checked ? 'completed' : null};
                            setSelectedTicket(updatedTicket);
                          }}
                        />
                        <span style={{color: '#333'}}>Fields Done</span>
                      </label>
                    </div>
                  )}
                  {selectedTicket.pressures && (
                    <div className="task-check">
                      <label>
                        <input
                          type="checkbox"
                          checked={selectedTicket.pressures_result === 'completed'}
                          onChange={(e) => {
                            const updatedTicket = {...selectedTicket, pressures_result: e.target.checked ? 'completed' : null};
                            setSelectedTicket(updatedTicket);
                          }}
                        />
                        <span style={{color: '#333'}}>IOPs Done</span>
                      </label>
                    </div>
                  )}
                  {selectedTicket.scans && (
                    <div className="task-check">
                      <label>
                        <input
                          type="checkbox"
                          checked={selectedTicket.scans_result === 'completed'}
                          onChange={(e) => {
                            const updatedTicket = {...selectedTicket, scans_result: e.target.checked ? 'completed' : null};
                            setSelectedTicket(updatedTicket);
                          }}
                        />
                        <span style={{color: '#333'}}>Scans Done</span>
                      </label>
                    </div>
                  )}
                </div>

                <div className="modal-section">
                  <h3>Notes & Findings</h3>
                  <textarea
                    className="modal-notes-textarea"
                    value={selectedTicket.notes || ''}
                    onChange={(e) => {
                      const updatedTicket = {...selectedTicket, notes: e.target.value};
                      setSelectedTicket(updatedTicket);
                    }}
                    placeholder="Add notes about findings, test results, referral reasons..."
                    rows="4"
                  />
                </div>

                <div className="modal-section">
                  <h3>Referral Status</h3>
                  <div className="task-check">
                    <label>
                      <input
                        type="checkbox"
                        checked={selectedTicket.referral || false}
                        onChange={(e) => {
                          const updatedTicket = {...selectedTicket, referral: e.target.checked};
                          setSelectedTicket(updatedTicket);
                        }}
                      />
                      <span style={{color: '#333'}}>Referral Needed</span>
                    </label>
                  </div>
                  {selectedTicket.referral && (
                    <div className="task-check" style={{marginLeft: '30px'}}>
                      <label>
                        <input
                          type="checkbox"
                          checked={selectedTicket.referral_sent || false}
                          onChange={(e) => {
                            const updatedTicket = {
                              ...selectedTicket,
                              referral_sent: e.target.checked,
                              referral_sent_date: e.target.checked ? new Date().toISOString() : null
                            };
                            setSelectedTicket(updatedTicket);
                          }}
                        />
                        <span style={{color: '#333'}}>Referral Sent</span>
                      </label>
                    </div>
                  )}
                </div>

                <div className="modal-buttons">
                  <button
                    onClick={() => {
                      handleUpdateTicket({
                        fields_result: selectedTicket.fields_result,
                        pressures_result: selectedTicket.pressures_result,
                        scans_result: selectedTicket.scans_result,
                        notes: selectedTicket.notes,
                        referral: true,
                        referral_sent: false,
                        ticket_status: 'open'
                      });
                    }}
                    className="btn-referral-later"
                  >
                    📋 Send Referral Later
                  </button>
                  <button onClick={() => setModalView('postpone')} className="btn-postpone">
                    Postpone
                  </button>
                  <button
                    onClick={() => {
                      handleUpdateTicket({
                        fields_result: selectedTicket.fields_result,
                        pressures_result: selectedTicket.pressures_result,
                        scans_result: selectedTicket.scans_result,
                        notes: selectedTicket.notes,
                        referral: selectedTicket.referral,
                        referral_sent: selectedTicket.referral_sent,
                        referral_sent_date: selectedTicket.referral_sent_date,
                        completed: true,
                        ticket_status: 'closed'
                      });
                      handleCloseTicket();
                    }}
                    className="btn-close-ticket"
                  >
                    All Tasks Completed
                  </button>
                  <button onClick={() => setShowTicketModal(false)} className="btn-cancel">
                    Cancel
                  </button>
                </div>
              </>
            )}

            {modalView === 'postpone' && (
              <>
                <h3>Postpone Ticket</h3>
                <input
                  type="date"
                  className="date-picker"
                  onChange={(e) => {
                    if (e.target.value) {
                      handlePostpone(new Date(e.target.value).toISOString());
                    }
                  }}
                />
                <div className="modal-buttons">
                  <button onClick={() => setModalView('main')} className="btn-cancel">
                    Back
                  </button>
                </div>
              </>
            )}

            {modalView === 'referral' && (
              <>
                <h3>Mark Referral as Sent?</h3>
                <div className="modal-buttons">
                  <button onClick={handleReferralSent} className="btn-success">
                    ✓ Yes, Referral Sent
                  </button>
                  <button onClick={() => setModalView('main')} className="btn-cancel">
                    Cancel
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;